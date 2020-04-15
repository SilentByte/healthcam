```
docker build . -t "foo:bar"
docker run --device=/dev/vchiq foo:bar
```
Should get the output
```zsh
Recording I guess?
['/home/test.mjpeg', '/home/foo.jpeg']
18069702
142834
```

Showing that you're able to write a video and a file.

I'll point out that currently I'm seeing this generally 1/3 times I try to run the container
```zsh
mmal: mmal_vc_port_enable: failed to enable port vc.null_sink:in:0(OPQV): ENOSPC
mmal: mmal_port_enable: failed to enable connected port (vc.null_sink:in:0(OPQV))0xbd2c50 (ENOSPC)
mmal: mmal_connection_enable: output port couldn't be enabled
Traceback (most recent call last):
  File "test.py", line 8, in <module>
    cam = PiCamera(camera_num=0)
  File "/usr/lib/python3/dist-packages/picamera/camera.py", line 433, in __init__
    self._init_preview()
  File "/usr/lib/python3/dist-packages/picamera/camera.py", line 513, in _init_preview
    self, self._camera.outputs[self.CAMERA_PREVIEW_PORT])
  File "/usr/lib/python3/dist-packages/picamera/renderers.py", line 558, in __init__
    self.renderer.inputs[0].connect(source).enable()
  File "/usr/lib/python3/dist-packages/picamera/mmalobj.py", line 2212, in enable
    prefix="Failed to enable connection")
  File "/usr/lib/python3/dist-packages/picamera/exc.py", line 184, in mmal_check
    raise PiCameraMMALError(status, prefix)
picamera.exc.PiCameraMMALError: Failed to enable connection: Out of resources
```
Would strongly suggest coding with the expectation that the first N times you try to get the camera, it fails and add a try loop in there.
