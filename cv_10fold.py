import sys, numpy
from algorithms.KNearestNeighbour import KNN
from algorithms.NaiveBayes import NaiveBayes

# Read data and store yes and no instances
def read_Data(filepath):
        yes_instances = []
        no_instances = []
        f = open(filepath, "r")
        lines = f.readlines()
        for line in lines:
            line = line.strip("\n").split(",")
            for i in range(0, len(line)):
                # Convert numeric values into float
                if line[i] != "yes" and line[i] != "no":
                    line[i] = float(line[i])
                elif line[i] == "yes":
                    yes_instances.append(line)
                elif line[i] == "no":
                    no_instances.append(line)
        f.close()
        return yes_instances, no_instances

# Creates 10 stratified folds with the data
def create_stratified_folds(yes_instances, no_instances):
    stratified_folds = dict()
    for i in range(10):
        stratified_folds[i] = []
    partition = 0
    while len(no_instances) > 0:
        partition += 1
        stratified_folds[partition % 10].append(no_instances.pop())
    while len(yes_instances) > 0:
        partition += 1
        stratified_folds[partition % 10].append(yes_instances.pop())
    return stratified_folds

def ten_fold_cv(folds):
    oneNN_accuracy = []
    fiveNN_accuracy = []
    nb_accuracy = []
    # print("YOOOO")
    # print(folds[0])
    for i in range(10):
        validation_instances = []
        for row_number in range(len(folds[i])):
            validation_instances.append([])
            for elements in folds[i][row_number] : 
                validation_instances[row_number].append(elements)


        training_instances = []
        for j in range(10):
            if j != i:
                training_instances += folds[j]

        # remove yes and no from each validation instance
        
        validation_outcomes = []
        for row in validation_instances:
            # print(row)
            validation_outcomes.append(row[-1]) 
            del row[-1]
        
        # print(folds[0])
        oneNN_results = KNN(1, validation_instances, training_instances)
        fiveNN_results = KNN(5, validation_instances, training_instances)
        nb_results = NaiveBayes(validation_instances, training_instances) # fails due to length of yes and no =0
        

        nb_correct = 0
        oneNN_correct = 0
        fiveNN_correct = 0
        for k in range(len(validation_instances)):
            if oneNN_results[k] == validation_outcomes[k]:
                oneNN_correct += 1
            if fiveNN_results[k] == validation_outcomes[k]:
                fiveNN_correct += 1
            if nb_results[k] == validation_outcomes[k]:
                nb_correct += 1
        
        oneNN_accuracy.append(oneNN_correct/len(validation_instances))
        fiveNN_accuracy.append(fiveNN_correct / len(validation_instances))
        nb_accuracy.append(nb_correct/len(validation_instances))

        print('Round {} accuracy for 1-Nearest Neighbours: {}'.format(i + 1, oneNN_accuracy[i]))
        print('Round {} accuracy for 5-Nearest Neighbours: {}'.format(i + 1, fiveNN_accuracy[i]))
        print('Round {} accuracy for Naive Bayes: {}'.format(i + 1, nb_accuracy[i]))

    oneNN_average = numpy.mean(oneNN_accuracy)
    fiveNN_average = numpy.mean(fiveNN_accuracy)
    nb_average = numpy.mean(nb_accuracy)

    print(" ")
    print('Average accuracy for 1-Nearest Neighbours: {}%'.format(oneNN_average))
    print('Average accuracy for 5-Nearest Neighbours: {}%'.format(fiveNN_average))
    print('Average accuracy for Naive Bayes: {}%'.format(nb_average))

def write_output_file(folds):
    with open('pima-folds.csv', 'w') as outfile:
        count = 0
        for fold in folds:
            count += 1
            outfile.write('fold{}\n'.format(count))
            for instance in folds[fold]:
                instance = str(instance).replace("[", "").replace("]", "").replace("'", "").replace(" ", "") + "\n"
                outfile.write(instance)
            if count < 10:
                outfile.write('\n')

if __name__ == "__main__":
    data_file = sys.argv[1]
    yes_instances, no_instances = read_Data(data_file)
    stratified_folds = create_stratified_folds(yes_instances, no_instances)
    #write_output_file(stratified_folds)
    ten_fold_cv(stratified_folds)