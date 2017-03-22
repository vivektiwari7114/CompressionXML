#Basic Programe Needs
import xml.etree.ElementTree as PT
import zlib
import sys
import httplib
import xml.dom.minidom


# Used to make the starting tag  along with the attributes
# Example : <books test= "1" id = "arr1" >
def makeNode(root):
    fileWrite.write("<" + root.tag)
    for item in root.attrib:
        key = item;
        value = root.attrib.get(item)
        fileWrite.write(" " + key + " = " + '"' + value + '"' + " ")
    fileWrite.write(">")

#Function to get the Contents that need to be gZiped
#Content that is marked with test="1"
def gZipContent(root):
    gZip = ""
    gZip += "<" + root.tag
    for item in root.attrib:
        key = item;
        value = root.attrib.get(item)
        gZip += " " + key + " = " + '"' + value + '"' + " "
    gZip += ">"
    gZip += root.text
    gZip += "</" + root.tag + ">"
    gZip += "]"
    compress = zlib.compressobj( -1)
    compressString = compress.compress(gZip)
    finalString = "[" + compressString + "]"
    return finalString
    #return gZip


#Function to end tag
# Example : </books>
def writeEndTag(root):
    fileWrite.write("</" + root.tag + ">")

#Recursive function that parses the entire XML
#Check whether the current element has test attribute with value 1
def parseXmlRecursive(root):
    makeNode(root)
    if root.attrib.has_key('test'):
        if root.attrib.get('test') == "1":
            if len(root._children) > 0:
                for children in root._children:
                    gZip = gZipContent(children)
                    fileWrite.write(gZip)
                writeEndTag(root)
            else:
                compress = zlib.compressobj(-1)
                textZipped = compress.compress(root.text)
                fileWrite.write("[" +textZipped + "]")
                #fileWrite.write(root.text)
                writeEndTag(root)
            return
    fileWrite.write(root.text)
    for parentItem in root._children:
        parseXmlRecursive(parentItem)
    writeEndTag(root)

def parseUnzip(root):
    makeNode(root)
    if root.attrib.has_key('test'):
        if root.attrib.get('test') == "1":
            if len(root._children) > 0:
                for children in root._children:
                    gZip = gZipContent(children)
                    fileWrite.write(gZip)
                writeEndTag(root)
            else:
                textZipped = zlib.compress(root.text)
                fileWrite.write(textZipped)
                #fileWrite.write(root.text)
                writeEndTag(root)
            return
    fileWrite.write(root.text)
    for parentItem in root._children:
        parseXmlRecursive(parentItem)
    writeEndTag(root)

#Create A post request to send XML File to the given EndPoint
def do_request(xml_location):
    HOST = "www.posttestserver.com"
    API_URL = "/post.php"
    request = open(xml_location, "r").read()

    webservice = httplib.HTTP(HOST)
    webservice.putrequest("POST", API_URL)
    webservice.putheader("Host", HOST)
    webservice.putheader("User-Agent", "Python post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(request))
    webservice.endheaders()

    webservice.send(request)

    statuscode, statusmessage, header = webservice.getreply()

    result = webservice.getfile().read()
    print (statuscode, statusmessage, header)
    print (result)



#Main Execution of the program
readFile = open(sys.argv[1],"r")
#option = sys.argv[2]
option = "--gzip"
fileWrite  = open('result.xml', 'w')
tree = PT.parse(readFile)
root = tree.getroot()
result = ""
if option == "--gzip":
    parseXmlRecursive(root)
elif option == "--gunzip":
    parseUnzip(root)
    print (root)
else:
    print ("Please delect a valid option --gzip/--gunzip")
#Send the XML newly created XML file to the post request
fileWrite.close()
do_request("result.xml")




#API_URL = "/api/url"



