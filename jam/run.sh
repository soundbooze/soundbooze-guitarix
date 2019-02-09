#!/bin/sh

killall guitarix > /dev/null 2>&1
killall jack_thru > /dev/null 2>&1

guitarix &
jack_thru &

sleep 3

jack_disconnect 'jack_thru:output_1' 'system:playback_1'
jack_disconnect 'jack_thru:output_2' 'system:playback_2'

jack_connect 'system:capture_1' 'gx_head_amp:in_0'

# guitarix -> convolver
jack_connect 'gx_head_fx:out_0' 'effect_1:in_1'
jack_connect 'gx_head_fx:out_1' 'effect_1:in_2'

# convolver -> playback
jack_connect 'effect_1:out_1' 'system:playback_1'
jack_connect 'effect_1:out_2' 'system:playback_2'

# convolver -> delay
jack_connect 'effect_1:out_1' 'effect_0:in_l' 
jack_connect 'effect_1:out_2' 'effect_0:in_r' 

jack_connect 'effect_0:out_l' 'system:playback_1'
jack_connect 'effect_0:out_r' 'system:playback_2'

# Jack Thru

# delay 
jack_connect 'effect_0:out_l' 'jack_thru:input_1'
jack_connect 'effect_0:out_r' 'jack_thru:input_2'

# convolver
jack_connect 'effect_1:out_1' 'jack_thru:input_1'
jack_connect 'effect_1:out_2' 'jack_thru:input_2'
