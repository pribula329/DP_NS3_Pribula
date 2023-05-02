import xml.sax
from xml.sax.xmlreader import XMLReader
from memory_profiler import profile
from time_profiler import timer
global handler

class NS3Handler(xml.sax.handler.ContentHandler):
    """
        Class for SAX Parser

    """
    def __init__(self):
        self.CurrentData = ""
        self.CurrentNode = ""
        self.address = []
        self.node = []
        self.nodeDesc = {}
        self.nodeAddress = {}
        self.nodeChangePos = []
        self.nodePos = []
        self.transport = []
        self.metaInfo= []
        self.transportTime = []
        self.CurrentCount = 0
        self.transportCount = 0
        self.wifiTransportHelp = {}


    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "node":
            id = attributes["id"]
            sysId = attributes["sysId"]
            locX = attributes["locX"]
            locY = attributes["locY"]
            self.node.append([int(id),int(sysId),float(locX),float(locY)])
            self.nodeDesc.update({id : id})
        if tag== "nu":
            node = attributes["id"]
            type = attributes["p"]
            if type=="d":
                self.nodeDesc.update({node : attributes["descr"]})
            if type=="p":
                id = int(attributes["id"])
                locX = float(attributes["x"])
                locY = float(attributes["y"])
                posUpdate = [id,locX,locY,self.transportCount]
                self.nodePos.append(posUpdate)
                self.nodeChangePos.append(self.transportCount)


        if tag == "ip":
            n = attributes["n"]
            self.CurrentNode = n

        if tag == "p":

            fId = attributes["fId"]
            tId = attributes["tId"]
            self.transport.append([fId,tId])
            self.transportCount += 1
            info = attributes["meta-info"]
            self.metaInfo.append(info)
            timeTransport = attributes["fbTx"]
            self.transportTime.append(timeTransport)
        if tag == "pr":
            uID = attributes["uId"]
            fId = attributes["fId"]
            fbTx = attributes["fbTx"]
            info = attributes["meta-info"]

            self.wifiTransportHelp.update({uID: [fId, fbTx, info]})

        if tag == "wpr":
            uID = attributes["uId"]
            wifiHelp = self.wifiTransportHelp.get(uID)
            fId = wifiHelp[0]
            tId = attributes["tId"]
            self.transport.append([fId,tId])
            self.transportCount += 1
            self.metaInfo.append(wifiHelp[2])
            self.transportTime.append(wifiHelp[1])


    # Call when an elements ends
    def endElement(self, tag):
        if tag == "ip":
            self.nodeAddress.update({self.CurrentNode: self.address})
            self.CurrentCount = 0
            self.CurrentNode = ""
            self.address = []
        self.CurrentData = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "address":
            self.address.append(content)
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
