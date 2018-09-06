from concurrent import futures
import time
import math
import sys

import grpc

import spacy_pb2
import spacy_pb2_grpc

import spacy

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#while True:
#    time.sleep(_ONE_DAY_IN_SECONDS)

class SpacyServicer(spacy_pb2_grpc.SpacyServServicer):
    """Provides methods that implement functionality of spacy server."""

    def __init__(self):
        self.nlp = spacy.load('en')

    def streamCommand(self, request_iterator, context):
        for new_cmd in request_iterator:
            print("recv %s" % (new_cmd.str))
            if new_cmd.cmd == spacy_pb2.NER:
                print("cmd is NER")
                cur_doc = self.nlp(new_cmd.str)
                lstner = []
                for ent in cur_doc.ents:
                    print(ent.text, ent.label_, ent.label)
                    lstner.append(spacy_pb2.NERInfo(ent=ent.text, labelstr=ent.label_, label=ent.label))
                replyner = spacy_pb2.ReplyNER()
                replyner.info.extend(lstner)
                sys.stdout.flush()
                yield spacy_pb2.ReplyCommand(cmd=spacy_pb2.NER, ReplyNER=replyner)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spacy_pb2_grpc.add_SpacyServServicer_to_server(
        SpacyServicer(), server)
    server.add_insecure_port('[::]:3733')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()