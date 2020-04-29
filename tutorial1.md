# Hypergan tutorial 1

Thanks for trying out hypergan. This tutorial will walk you through creating your first model, exploring it, and building/deploying the generator.

## Acquiring a dataset

You can acquire a dataset by having a folder full of loose images.

TODO: instructions for downloading dataset

## Getting started

First install tensorflow and hypergan.

## Testing install

To test tensorflow is installed correctly, start a python session and run `import tensorflow as tf`.

To test hypergan is installed correctly, run `hypergan new . -l`

You can view video card usage with `nvidia-smi`

## Training hypergan

You can run:

```text
  hypergan train -c online256 -s 256x256x3 -format png --sampler static_batch --sample_every 10 /path/to/data
```

Once hypergan is working, you can sample your

## Sampling your model

You've created an infinite manifold. Great! With any luck it's diverse. You can see how diverse your model is by using:

```text
  hypergan sample -c online256 -s 256x256x3 -format png --sampler random_walk /path/to/data
```

## Building your model

```text
  hypergan build -c online256 -s 256x256x3 -format png --sampler batch --sample_every 10 /path/to/data
```

## Deploying your model

You've made a great model you'd like to share. Awesome! You can deploy it to users through a few methods.

### Deploy to android

TODO: instructions

Come on over to our discord and share what you've created!

