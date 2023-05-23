<launch>

  <!-- Start bot_1 -->
  <node pkg="PSO_pkg" type="bot_1_node.py" name="bot_1" output="screen" />

  <!-- Wait for bot_1 to start before starting bot_2 -->
  <node pkg="PSO_pkg" type="bot_2_node.py" name="bot_2_wait" args="launch --wait-for bot_1 bot_nodes.launch.py bot:=bot_2" output="screen">
    <remap from="bot" to="bot_2" />
  </node>

  <!-- Wait for bot_2 to start before starting bot_3 -->
  <node pkg="PSO_pkg" type="bot_3_node.py" name="bot_3_wait" args="launch --wait-for bot_2 bot_nodes.launch.py bot:=bot_3" output="screen">
    <remap from="bot" to="bot_3" />
  </node>

  <!-- Wait for bot_3 to start before starting bot_4 -->
  <node pkg="PSO_pkg" type="bot_4_node.py" name="bot_4_wait" args="launch --wait-for bot_3 bot_nodes.launch.py bot:=bot_4" output="screen">
    <remap from="bot" to="bot_4" />
  </node>

  <!-- Wait for bot_4 to start before starting bot_5 -->
  <node pkg="PSO_pkg" type="bot_5_node.py" name="bot_5_wait" args="launch --wait-for bot_4 bot_nodes.launch.py bot:=bot_5" output="screen">
    <remap from="bot" to="bot_5" />
  </node>

  <!-- Start the aggregator node -->
  <node pkg="PSO_pkg" type="aggregator_node.py" name="aggregator" output="screen" />

</launch>

