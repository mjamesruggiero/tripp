from __future__ import division
import algebra
import math


def step_function(x):
    return 1 if x >= 0 else 0


def perceptron_output(weights, bias, x):
    """returns 1 if the perceptron 'fires'; 0 if not"""
    return step_function(algebra.dot(weights, x) + bias)


def sigmoid(t):
    return 1 / (1 + math.exp(-t))


def neuron_output(weights, inputs):
    return sigmoid(algebra.dot(weights, inputs))


def feed_forward(neural_network, input_vector):
    """takes a neural_network (represented as a
    list of list of lists of weights) and returns the output
    from forward-propagating the input"""
    outputs = []

    for layer in neural_network:
        # add bias of [1]
        input_with_bias = input_vector + [1]
        output = [neuron_output(neuron, input_with_bias)
                  for neuron in layer]

        outputs.append(output)

        input_vector = output

    return outputs


def backpropogate(network, input_vector, target):
    hidden_outputs, outputs = feed_forward(network, input_vector)

    # the output * (1 - output) is from the derivative of sigmoid
    output_deltas = [output * (1 - output) * (output - target[i])
                     for i, output in enumerate(outputs)]

    # adjust weights for output layer (network[-1])
    for i, output_neuron in enumerate(network[-1]):
        for j, hidden_output in enumerate(hidden_outputs + [1]):
            output_neuron[j] -= output_deltas[i] * hidden_output

    hidden_deltas = [hidden_output * (1 - hidden_output) *
                     algebra.dot(output_deltas, [n[i] for n in network[1]])
                     for i, hidden_output in enumerate(hidden_outputs)]

    for i, hidden_neuron in enumerate(network[0]):
        for j, input in enumerate(input_vector + 1):
            hidden_neuron[j] -= hidden_deltas[i] * input
