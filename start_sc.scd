#!/usr/local/bin/sclang

var channelMap = [1, 2, 4, 5]; //change this map if necessary!
//var channels = Array.fill(4, 1);
var passThru = Array.new(4);
var maxChan = 6; //TODO ta bort

s.options.numInputBusChannels = 6;
s.options.numOutputBusChannels = 6;

SynthDef.new("piMixer", {
	arg channel=0, vol=1;
	var input = SoundIn.ar(channel, 1);
	Out.ar(channel%maxChan, input*vol); //TODO ta bort maxChan...
}).add;

thisProcess.addOSCRecvFunc(
	{ |msg, time, addr|
		if (msg[0] == '/channel'){
			//channels[msg[1]] = (channels[msg[1]]+1)%2;
			//passThru[msg[1]].set(\vol, channels[msg[1]]);
			// postf("% received\n% is new value\n", msg[1], channels[msg[1]]); // DEBUG
			// postf("% and %\n", channels, msg[1]);
            msg[1..].do({
                arg val, index;
                passThru[index].set(\vol, val);
            });
		}
	}
);

s.waitForBoot({
	Synth.new(\piMixer); // syrsor ...

	channelMap.do({
		arg val, index;
		//postf("% and %", i, val);
		passThru.add(Synth.new(\piMixer, [\channel, val]));
	});
	// postf("%\n", passThru);

	postln("Booted");
	// s.meter; // TODO TA BORT!!!
});

