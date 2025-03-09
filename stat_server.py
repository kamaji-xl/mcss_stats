import zmq
import random

PORT = 5252


def calculate(req):
    data = req["data"]
    roll_ctr = len(data)
    pass_ctr = 0
    fail_ctr = 0
    roll_sum = 0

    if len(data) > 0:
        for roll in data:
            roll_sum += roll[0]
            if roll[2] == "Pass":
                pass_ctr += 1
            elif roll[2] == "Fail":
                fail_ctr += 1

        avg_roll = round(roll_sum / roll_ctr)
        pass_percent = round((pass_ctr / roll_ctr) * 100, 2)
        fail_percent = round((fail_ctr / roll_ctr) * 100, 2)
        res = {
            "status": "success",
            "avg_roll": avg_roll,
            "pass_percent": pass_percent,
            "fail_percent": fail_percent
        }
    else:
        res = {"status": "error"}

    return res


def stat_request_handler(req):
    if req["command"] == "calculate":
        res = calculate(req)
    else:
        res = {"status": "error"}

    return res


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{PORT}")

    print(f"Listening on port tcp://localhost:{PORT}")

    stats = {}

    while True:
        try:
            request_json = socket.recv_json()
            print(request_json)
            response = stat_request_handler(request_json)
            print(f"\nsending response:")

            for key in response.keys():
                print(f"\t{key}: {response[key]}")

            socket.send_json(response)
        except zmq.error.ZMQError as e:
            print("ZMQ Error:", e)
