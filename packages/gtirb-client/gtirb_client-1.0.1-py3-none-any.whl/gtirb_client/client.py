import argparse
import json
import logging
import sys
import time
import typing
import uuid
from http import HTTPStatus

import requests

from .common import JobStatus
from .version import __version__

logger = logging.getLogger(__name__)


class JobInfo(typing.NamedTuple):
    status: JobStatus
    success: typing.Optional[bool]
    error: typing.Optional[str]
    stdout: typing.Optional[str]
    stderr: typing.Optional[str]
    outputs: typing.Optional[typing.Dict[str, typing.List[str]]]


class OutputOf:
    def __init__(self, job: "Job", kind: str) -> None:
        self.job = job
        self.kind = kind

    def as_json(self) -> dict:
        return {
            "job": str(self.job.id),
            "kind": self.kind,
        }


class Job:
    def __init__(self, client: "GSPClient", id_: uuid.UUID) -> None:
        self.client = client
        self.id = id_

    @property
    def info(self) -> JobInfo:
        logger.info("getting status for job %s" % self.id)
        response = requests.get(self.client.url + "/job?job=%s" % self.id)
        if not response.ok and response.status_code != HTTPStatus.NOT_FOUND:
            raise IOError(response.content.decode("utf-8"))
        status: typing.Dict[str, typing.Any] = json.loads(response.content)
        logger.info(
            "status for job %s retrieved: %s" % (self.id, status["status"])
        )
        return JobInfo(
            status=JobStatus(status["status"]),
            **{
                k: status.get(k)
                for k in ["success", "error", "stdout", "stderr", "outputs"]
            }
        )

    def get_output(self, file_id: str) -> bytes:
        logger.info("getting file %s for job %s" % (file_id, self.id))
        response = requests.get(
            self.client.url + "/job/file?job=%s&file=%s" % (self.id, file_id)
        )
        if not response.ok:
            raise IOError(response.content.decode("utf-8"))
        return response.content

    @property
    def logs(self) -> typing.List[typing.Tuple[str, str]]:
        logger.info("getting logs for job %s" % self.id)
        response = requests.get(self.client.url + "/job/log?job=%s" % self.id)
        if not response.ok:
            raise IOError(response.content.decode("utf-8"))
        return [
            (logline[0], logline[1])
            for logline in json.loads(response.content)
        ]


def _spec_to_json(spec: typing.Union[str, typing.IO, OutputOf]):
    if isinstance(spec, str):
        return spec
    elif isinstance(spec, OutputOf):
        return spec.as_json()
    else:
        return spec.name


class Transform(typing.NamedTuple):
    name: str
    version: str
    inputs: typing.List[str]
    outputs: typing.List[str]


class GSPClient:
    def __init__(self, url: str = "http://0.0.0.0:80") -> None:
        self.url = url

    def submit_job(
        self,
        xform: str,
        inputs: typing.Dict[
            str, typing.Iterable[typing.Union[str, typing.IO, OutputOf]]
        ] = {},
        args: typing.Iterable[str] = (),
    ) -> Job:
        logger.info("Submitting job for transform %s" % xform)
        attachments: typing.Dict[str, typing.IO] = {}
        for files in inputs.values():
            for input in files:
                if isinstance(input, str):
                    attachments[input] = open(input, "rb")
                elif not isinstance(input, OutputOf):
                    attachments[input.name] = input

        response = requests.post(
            self.url + "/job",
            files={
                "transform": json.dumps(
                    {
                        "transform": xform,
                        "inputs": {
                            k: [_spec_to_json(x) for x in v]
                            for k, v in inputs.items()
                        },
                        "arguments": args,
                    }
                ),
                **attachments,
            },
        )

        if not response.ok:
            raise IOError(response.content.decode("utf-8"))

        job = Job(self, uuid.UUID(json.loads(response.content)["job"]))
        logger.info("Submitted job %s successfully" % job.id)
        return job

    def get_job(self, id_: uuid.UUID) -> Job:
        return Job(self, id_)

    @property
    def transforms(self) -> typing.List[Transform]:
        logger.info("getting transform list")
        response = requests.get(self.url + "/transforms")
        if not response.ok:
            raise IOError(response.content.decode("utf-8"))
        return [Transform(**xform) for xform in json.loads(response.content)]


class KeyValue:
    def __init__(self, arg: str) -> None:
        args = arg.split("=")
        if len(args) != 2:
            raise argparse.ArgumentTypeError(
                "value must be of form 'kind=filename'"
            )
        self.key = args[0]
        self.value = args[1]


class KeyJobKind:
    def __init__(self, arg: str) -> None:
        args = arg.split("=")
        if len(args) != 3:
            raise argparse.ArgumentTypeError(
                "value must be of form 'inkind=job=outkind'"
            )
        self.key = args[0]
        self.job = args[1]
        self.value = args[2]


def main(argv: typing.List[str] = sys.argv) -> int:
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s]\t%(message)s"
    )

    parser = argparse.ArgumentParser(prog=argv[0])
    parser.add_argument(
        "--version",
        "-v",
        help="Print version and exit",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "url", help="The URL to connect to", type=str,
    )
    parser.add_argument(
        "--xforms",
        help="Print list of transforms on server and exit",
        action="store_true",
    )
    parser.add_argument(
        "xform", help="The transform to invoke", type=str, nargs="?"
    )
    parser.add_argument(
        "--input",
        help="Add an input to an input kind",
        type=KeyValue,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--pipe",
        help="Pipe an output of another job into an input of this job",
        type=KeyJobKind,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--output",
        help="Save an output from an output kind to a file pattern",
        type=KeyValue,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--arg",
        help="Add an additional argument",
        type=str,
        action="append",
        default=[],
    )
    parser.add_argument(
        "--logs", help="Save logs to file", type=str, default=None,
    )

    args = parser.parse_args(argv[1:])
    client = GSPClient(args.url)

    if args.xforms:
        for xform in client.transforms:
            logger.info(xform.name)
            logger.info("\tVersion: %s" % xform.version)
            logger.info("\tInput kinds: %s" % " ".join(xform.inputs))
            logger.info("\tOutput kinds: %s" % " ".join(xform.outputs))
        return 0
    else:
        if args.xform is None:
            logger.error("required argument xform is missing")
            logger.error("use the --help option for info")
            return 1

    inputs = {}
    for kv in args.input:
        inputs.setdefault(kv.key, [])
        inputs[kv.key].append(kv.value)
    for kjk in args.pipe:
        inputs.setdefault(kjk.key, [])
        inputs[kjk.key].append(OutputOf(client.get_job(kjk.job), kjk.value))
    outputs = {}
    for kv in args.output:
        outputs[kv.key] = kv.value
    job = client.submit_job(args.xform, inputs, args.arg)
    while True:
        info = job.info
        if info.status == JobStatus.COMPLETED:
            if args.logs is not None:
                if args.logs == "-":
                    for logtype, msg in job.logs:
                        print(
                            msg,
                            end="",
                            file=sys.stderr
                            if logtype == "stderr"
                            else sys.stdout,
                        )
                else:
                    with open(args.logs, "w") as stream:
                        stream.write("".join(msg for logtype, msg in job.logs))
            logger.info("Job complete! Successful? %s" % info.success)
            if not info.success:
                logger.error(info.error)
                return 1
            else:
                logger.info("Got outputs:")
                for kind, files in info.outputs.items():
                    logger.info("\t%s:" % kind)
                    for file in files:
                        logger.info("\t\t%s" % file)
                        if kind in outputs:
                            with open(
                                outputs[kind].replace("{}", file), "wb"
                            ) as stream:
                                stream.write(job.get_output(file))
                return 0
        if info.status == "expired":
            logger.error("Job expired before completion")
            return 1
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
