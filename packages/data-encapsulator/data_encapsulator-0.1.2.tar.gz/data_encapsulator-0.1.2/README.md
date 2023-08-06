# README #

This repostitory provides data encapsulation for websockets used by the EmbeddedJetson API

### How do I get set up? ###

```
pip3 install git+https://bitbucket.org/eheyeinc/data_encapsulator/src/main/
```

Example use of get\_next\_frame\_data() in websocket onMessage in Smart MSG client (Jackfruit/)
```
websocket onMessage(message)
    de = DataEncapsulator()
    de.add_to_buffer(message)     # add message string to previous buffer contents
    next_frame = de.get_next_frame_data()
    while next_frame  # {"type": payload_type, "data": payload}
          switch payload_type:
              process next_frame ...
                  next_frame = de.get_next_frame_data()
```
For fast test, uncomment the following and debug this file

```
try:
  de = DataEncapsulator()
  json_str = json.dumps({"key": "value"})
  json_str2 = json.dumps({"key": "value", "key2": "value2"})
  frame_out = de.create_data_frame("data_type_AAA", json_str)
  frame_out2 = de.create_data_frame("data_type_BBB", json_str2)
  frame_out3 = de.create_data_frame("data_type_CCC", json_str2)
  frame_out3 = frame_out3[4:]  #simulate data loss/corruption - should ignore this frame

  # create fake data on socket receive side
  de.add_to_buffer(f'junk{frame_out}{frame_out2}{frame_out3}morejunk{frame_out}')

  next_frame = de.get_next_frame_data()
  while next_frame:  # {"type": payload_type, "data": payload}
          print(next_frame)
          next_frame = de.get_next_frame_data()
except Exception as e:
  print(f'frame_data general error trap: {e}')
```
### Who do I talk to? ###

* Steve Mason
