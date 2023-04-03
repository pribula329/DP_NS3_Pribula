import xml.sax
from xml.sax.xmlreader import XMLReader

global handler

class NS3Handler(xml.sax.handler.ContentHandler):
    """
        Class for SAX Parser

    """
    def __init__(self):
        self.CurrentData = ""
        self.address = ""
        self.node = []
        self.nodeDesc = {}
        self.transport = []
        self.metaInfo= []
        self.transportTime = []
        self.CurrentCount = 0
        self.transportCount = 0


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "node":
            print("*****Node*****")
            id = attributes["id"]
            sysId = attributes["sysId"]
            locX = attributes["locX"]
            locY = attributes["locY"]
            print("ID:", id)
            print("SysId:", sysId)
            print("LocX:", locX)
            print("LocY:", locY)
            self.node.append([int(id),int(sysId),float(locX),float(locY)])
            self.nodeDesc.update({id : id})
        if tag== "nu":
            node = attributes["id"]
            type = attributes["p"]
            if type=="d":
                self.nodeDesc.update({node : attributes["descr"]})

        if tag == "ip":
            print("*****IP*****")
            n = attributes["n"]
            print("ID ip:", n)
        if tag == "p":
            print("***** P *****")
            fId = attributes["fId"]
            tId = attributes["tId"]
            print("fId:", fId)
            print("tId:", tId)
            self.transport.append([int(fId),int(tId)])
            self.transportCount += 1
            print("Transport count:", self.transportCount)
            info = attributes["meta-info"]
            print(info)
            self.metaInfo.append(info)
            timeTransport = attributes["fbTx"]
            self.transportTime.append(timeTransport)



    # Call when an elements ends
    def endElement(self, tag):
        if self.CurrentData == "address":
            print("Address:", self.address)
        if tag == "ip":
            print("Count of address:", self.CurrentCount)
            self.CurrentCount = 0
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "address":
            self.address = content
            value = count(self.CurrentCount)
            self.CurrentCount = value


def count(num):
    num += 1
    return num


def read_sax_parser(path):
    """
        Function for read file with sax parser method
        :param path: path to file

    """
    global handler

    saxParser: XMLReader = xml.sax.make_parser()
    # turn off namepsaces
    saxParser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    handler = NS3Handler()
    saxParser.setContentHandler(handler)
    saxParser.parse(open(path))
    print(handler.node)
