import cv2
import base64
import json
import requests
import asyncio
import websockets

loop = asyncio.get_event_loop()
uri = "ws://localhost:8080"
websocket = loop.run_until_complete(websockets.connect(uri))


# settings for immersal sdk api
url = "https://api.immersal.com/1.15.0"
token = "52df255a3971bd4062048b1fed79494f7af9281270b1fffce4bfe30d3520d823"
email = "tatsuromurata317@gmail.com"
password = "rtfd2018"
mapId = 42209

cap = cv2.VideoCapture("IMG_1118.MOV")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(cv2.CAP_PROP_FPS, 10)
print(f"size: ({width}, {height})")


def ServerLocalize(url, token, b64img, mapId=42209):
    complete_url = url + '/localizeb64'

    data = {
        "token": token,
        "fx": 1455.738159, # image focal length in pixels on x axis
        "fy": 1455.738159, # image focal length in pixels on y axis
        "ox": 962.615967, # image principal point on x axis
        "oy": 694.292175, # image principal point on y axis
        "b64": str(b64img, "utf-8"), # base64 encoded .png image
        "mapIds": [{"id": mapId}] # a list of map ids to localize against
    }

    json_data = json.dumps(data)

    r = requests.post(complete_url, data=json_data)
    # print(r.text)
    rj = r.json()
    for k, v in rj.items():
        rj[k] = str(v)

    return json.dumps(rj).encode()


frame_count = 0
frame_freq = 20

while True:

    ret, frame = cap.read()

    if ret:
        if frame_count % frame_freq == 0:
            packet = json.dumps({"success": "false"}).encode()
            loop.run_until_complete(websocket.send(packet))
            received_packet = loop.run_until_complete(websocket.recv())

            retval, buffer = cv2.imencode(".png", frame)
            png_as_str = base64.b64encode(buffer)

            result = ServerLocalize(url, token, png_as_str, mapId)
            print(result)
            # print(png_as_str)
            packet = result
            loop.run_until_complete(websocket.send(packet))

        cv2.imshow("frame", frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

loop.run_until_complete(websocket.close())
loop.close()
print("Finish.")


"""
# reponses
data1106 = {
	"error":	"none",
	"success":	True,
	"map":	41769,
	"px":	-0.46422445774078369,
	"py":	-0.1678304523229599,
	"pz":	-0.58463960886001587,
	"r00":	-0.10892344266176224,
	"r01":	0.050383813679218292,
	"r02":	-0.99277245998382568,
	"r10":	0.024300536140799522,
	"r11":	-0.99828124046325684,
	"r12":	-0.053329557180404663,
	"r20":	-0.99375307559967041,
	"r21":	-0.029933741316199303,
	"r22":	0.10751187056303024,
	"time":	0.659048038
}
"""
