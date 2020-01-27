import zmq
import msgpack
import subprocess
import time

class CapturePupil:
    """Class which takes care of pupil tracking. NOTE: NEEDS pupil service running!"""
    def __init__(self):
        #self.pid=subprocess.Popen(
        #    "C:\\Users\\localadmin\\PycharmProjects\\OddballPupillometry\\pupilCapture_V1.19_Winx64\\pupil_capture.exe")
        #time.sleep(5) #waits until pupil_service is executed
        #ADD Calibration here

        self.ctx = zmq.Context()
        # The REQ talks to Pupil remote and receives the session unique IPC SUB PORT
        self.pupil_remote = self.ctx.socket(zmq.REQ)

        # ip = 'localhost'  # If you talk to a different machine use its IP.
        self.ip = "localhost"#"10.253.153.12"
        self.port = 50020  # The port defaults to 50020. Set in Pupil Capture GUI.
        self.pupil_remote.connect(f'tcp://{self.ip}:{self.port}')

        print(self.ip)



        # Request 'SUB_PORT' for reading data
        self.pupil_remote.send_string('SUB_PORT')
        self.sub_port = self.pupil_remote.recv_string()



        # Request 'PUB_PORT' for writing data
        self.pupil_remote.send_string('PUB_PORT')
        pub_port = self.pupil_remote.recv_string()

        # start eye windows
        note = {'subject': 'eye_process.should_start', 'eye_id': 0, 'args': {}}
        print(self.send_recv_notification(note))
        time.sleep(2)

        # Assumes `sub_port` to be set to the current subscription port
        self.subscriber = self.ctx.socket(zmq.SUB)
        self.subscriber.connect(f'tcp://{self.ip}:{self.sub_port}')
        self.subscriber.subscribe('pupil.0')  # receive pupil messages (one eye only!)

    def getPupildiameter(self):
        topic, payload = self.subscriber.recv_multipart()
        message = msgpack.loads(payload)
        diam = message[b'diameter_3d'] #read-out the diameter according to 3D pupil model.
        return diam

    def send_recv_notification(self, n):
        topic = 'notify.' + n['subject']
        payload = msgpack.dumps(n)
        self.pupil_remote.send_string(topic, flags=zmq.SNDMORE)
        self.pupil_remote.send(payload)
        return self.pupil_remote.recv()

