# Run the Sensor Interface
# Get Equation Image from Sensor
# Turn into Image
# Run the Google Cloud Vision
# Get the text from Google Cloud Vision from Image
# Run the Wolfram Alpha
# Get answer from Wolfram Alpha from text
# Display the answer in Web App or Console

# Google API Key:

from google.cloud import vision

from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
import httplib2
import wap
import io
import time
import base64
import os.path

import server
import runTheserver

# for ui:
import Window

debug = False;
class Calculator:
    __APP_ID = "E3KYJG-QL67X8638A"  # App ID for Wolfram Engine
    __SERVER = "http://api.wolframalpha.com/v2/query?"  # Server for Wolfram Engine
    __ACC = 0.75

    __engine = None
    __vision = None
    __service = None

    def __init__(self):
        # credentials = GoogleCredentials.get_application_default().create_scoped(
            # ['http://www.googleapis.com/auth/cloud-platform'])
        # credentials.authorize(httplib2.Http())

        # self.__service = build('vision', 'v1', httplib2.Http(), developerKey="AIzaSyBim6cjT-mObrPjMaS4qhTn2Qdk6idSyZc")
        self.__engine = wap.WolframAlphaEngine(self.__APP_ID, self.__SERVER)
        self.__vision = vision.Client("Hacktech")

    def solve(self, image):
        equation = self.__detect_equation(image)  # Try to detect an equation
        if equation is None:  # If no equation was detected, then return None
            return None, None
        print "Equation: ", equation.encode('utf_8'), "|"
        solution = self.__query_equation(equation.encode('utf_8'))  # Try to solve the equation
        return equation, solution  # return the equation and solution

    def __query_equation(self, equation):
        if isinstance(equation, unicode):  # If the equation is in unicode, don't bother (Wolfram error occurs)
            return None
        query = self.__engine.CreateQuery(equation)  # Create a query for Wolfram
        wap.WolframAlphaQuery(query,self.__APP_ID)
        result = self.__engine.PerformQuery(query)  # Perform the query and get the result
        if debug: print "RESULT: ", result
        res = wap.WolframAlphaQueryResult(result)
        clean = self.__clean_result(res)  # Clean the result, and get the relevant points (like the solution)
        return clean if clean else None
        # return [wap.Pod(x).Title()[0] for x in res.Pods()], res.DataTypes()[0]

    def __detect_equation(self, image_path):
        """
        image = self.__read_file(image_path)
        req = self.__service.images().annotate(
            body={
                'requests': [{
                    'image': {
                        'content': image
                    },
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 5,
                    }]
                }]
            }
        )
        response = req.execute()
        for results in response['responses']:
            if 'labelAnnotations' in results:
                for annotations in results['labelAnnotations']:
                    print('Found label %s, score = %s' % (annotations['description'],annotations['score']))
        return ""
        """
        # """
        image = self.__read_file(image_path)  # Open the image file
        img = self.__vision.image(content=image)  # Get the image
        texts = img.detect_text()  # Try to detect text in the image
        if debug:
            for text in texts:
                print "Text Description: ", text.description
        return self.__filter_texts(texts)  # Filter the texts, get the most likely one
        # """

    def __read_file(self, path):
        with io.open(path, 'rb') as fi:
            # image = base64.b64encode(fi.read())
            image = fi.read()
        return image

    def __filter_texts(self, texts):
        c = lambda x, y: int((x.score - y.score) * 1 / self.__ACC)  # Sort based on the text's score
        texts.sort(c)
        return texts[0].description if len(texts) else None  # Get the most likely one

    def __clean_result(self, solution):
        data_type = solution.DataTypes()[0]  # Get the Data Type of the input
        if data_type == u"Math":  # Problems like 1 + 1 = ?
            # Useful stuff: Result
            pod = self.__find_pod(solution.Pods(), u"Result")
            if pod is None:
                return False
        elif data_type == u"Geometry":  # Problems like x + y = 1, xy = 1
            # Useful stuff: Solution, Geometric Figure
            pod = self.__find_pod(solution.Pods(), u"Real solution")
            if pod is None:
                pod = self.__find_pod(solution.Pods(), u"Solution")
                if pod is None:
                    return False
        elif data_type == u"MathematicalFunctionIdentity":  # Problems like cos(x), cos(1)
            # Useful stuff: Roots ?
            pod = self.__find_pod(solution.Pods(), u"Roots")
            if pod is None:
                return False
        elif data_type == u"D":  # Problems like derivative(x), differentiate(x + y)
            # Useful stuff: Derivative, Partial Derivatives
            pod = self.__find_pod(solution.Pods(), u"Derivative")
            if pod is None:
                pod = self.__find_pod(solution.Pods(), u"Partial derivatives")
                if pod is None:
                    return False
        elif data_type == u"Surface":  # Problems like xy + z = 1
            # Useful stuff: Solution, Geometric Figure
            pod = self.__find_pod(solution.Pods(), u"Solution")
            if pod is None:
                return False
        else:  # Problems that have no data type, like integrals, and singular variable equations
            # Useful stuff: Solution, Indefinite Integral
            pod = self.__find_pod(solution.Pods(), u"Solution")
            if pod is None:
                pod = self.__find_pod(solution.Pods(), u"Indefinite integral")
                if pod is None:
                    return False
        plain = self.__find_plain(pod.Subpods())
        return plain if plain is not None else False

    def __find_pod(self, pods, title):  # Look for a pod whose title matches the given title
        for pod in pods:
            pod = wap.Pod(pod)
            if pod.Title()[0] == title:
                return pod
        return None

    def __find_plain(self, sub_pods):  # Look for a plaintext subpod
        for sub in sub_pods:
            sp = wap.Subpod(sub)
            if len(sp.Plaintext()):
                return sp.Plaintext()[0]
        return None

if __name__ == '__main__':
    # """
    C = Calculator()
    Window.init()
    while True:
        while True:
            r = os.path.exists("real_life.png")
            time.sleep(1)
            # print r
            # print "In while"
            if r:
                # raw_input("FOUND FILE")
                break

        equation = ""
        answer = ""
        img = "real_life.png"
        print "Getting answer"
        equation, answer = C.solve(img)
        print "ANSWER: ", answer

        newDisplay = Window.Display(img, equation, answer)

        os.remove("real_life.png")
        time.sleep(1)
        exit()
        print "waiting for image..."
    # """
    """
    C = Calculator()
    while True:
        q = raw_input("EQ: ")
        if q == "d":
            debug = True
        else:
            for i in range(0,4):
                img = "meq_test_" + str(i + 1) + ".jpg"
                print C.solve(img)
                time.sleep(1)
                """
    # run()
