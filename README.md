# NLP-Project-Perceptron-classifier
Perceptron Classifier:Applying perceptron classifier on Binary classification of emails into ham and spam.

It describe in detail the implementation of a standard binary perceptron classifier, and an averaged binary perceptron classifier with the categories spam and ham (i.e., not spam). 

per_learn.py will learn a perceptron model from labeled data using the standard training algorithm.

per_classify.py will use a stored perceptron model to classify new data. per_learn.py and avg_per_learn.py will be invoked in the following way:

>python3 per_learn.py /path/to/input

avg_per_learn.py will learn a perceptron model from labeled data using the averaged perceptron training algorithm.

>python3 avg_per_learn.py /path/to/input
