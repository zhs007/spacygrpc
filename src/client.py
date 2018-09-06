import grpc

import spacy_pb2
import spacy_pb2_grpc

def generate_messages():
    messages = [
        spacy_pb2.Command(cmd=spacy_pb2.NER, str="Rami Eid is studying at Stony Brook University in New York"),
        spacy_pb2.Command(cmd=spacy_pb2.NER, str="update dtdemo server"),
    ]
    for msg in messages:
        print("%s" % (msg.str))
        yield msg

def proc_cmd(stub):
    responses = stub.streamCommand(generate_messages())
    for response in responses:
        print("recv")
        for curner in response.ReplyNER.info:
            print("%s %s %d" % (curner.ent, curner.labelstr, curner.label))


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:3733') as channel:
        stub = spacy_pb2_grpc.SpacyServStub(channel)
        proc_cmd(stub)


if __name__ == '__main__':
    run()