# Use Ray for multithread with python

## Install & run

Make a virtualenv with python 3, run `pip install -r requirements.txt`.

Run with `python remote_class_1.py`, parameters:
* `--followers 2`
* `--start 30` first value computed will be `fibonacci(30)`
* `--end 38` last value computed will be `fibonacci(38)`
* or run `python remote_class_1.py --help` for list of parameters

## Leader

The leader has a list of its followers.
The leader ask followers to run some computation then wait for results.
As soon as a result is processed, it's printed, the follower is asked to compute on a new value.

## Follower

The follower has no knowledge of the leader.
The follower class has the `ray.remote` annotation.

## Notes

* a follower computes a value only when asked to do so, no internal thread that keeps computing stuff
* use `htop` to see cpu usage, quite interesting

## Resources

* Ray example with A3C, kinda a bit complex to get started [official doc, a3c example](https://docs.ray.io/en/latest/auto_examples/plot_example-a3c.html)

## Why going through the trouble?

I adapted this code ([A3C with tensorflow](https://blog.tensorflow.org/2018/07/deep-reinforcement-learning-keras-eager-execution.html)) to tensorflow 2. It's great for understanding and it's limited to python multi-processing.
To get better speed, I thought the first step would be to use multi-threading. It's a smaller step than going straight to distributed.
Ray framework may deliver that.
