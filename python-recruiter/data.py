import numpy
import report


def clean(subject_info):
    result = {}
    subject_parameters = ["given-name", "last-name", "age", "traits-positive", "traits-neutral", "traits-negative",
                          "college-degree", "college-major", "position", "experience", "strengths", "weaknesses", "hours"]

    for index in range(len(subject_info)):
        if isinstance(subject_info[index], str) or isinstance(subject_info[index], float):
            result[subject_parameters[index]] = subject_info[index]
        else:
            temp0 = []
            for value in subject_info[index]:
                temp0.append(value)

            result[subject_parameters[index]] = temp0

    return result


def display(subject_info):
    subject_info = clean(subject_info)
    subject_parameters = ["given-name", "last-name", "age", "traits-positive", "traits-neutral", "traits-negative",
                          "college-degree", "college-major", "position", "experience", "strengths", "weaknesses", "hours"]

    print("Subject Info: ")
    for parameter in subject_parameters:
        print("\t{:20}: {}".format(parameter, subject_info[parameter]))


def match(subject_info):
    subject_info = clean(subject_info)

    # References
    degree_values = {"None": 0.0, "Associate": 0.3,
                     "Bachelor": 0.6, "Master": 1.0}

    major_indeces = {"None": 1, "Computer Science": 1, "Communications": 2, "Business": 3,
                     "Economics": 4, "English": 5, "Psychology": 6,
                     "Electrical Engineering": 7, "Mathematics": 8, "Marketing": 9}
    position_indeces = {"None": 1, "Junior Software Engineer": 1, "Software Engineer": 2, "Data Analyst": 3, "Data Scientist": 4,
                        "Social Media Manager": 5, "Sales Representative": 6, "Human Resources Specialist": 7,
                        "IT Consultant": 8, "Management Consultant": 9, "Business Adviser": 10,
                        "Project Manager": 11, "Risk Manager": 12, "Statistician": 13,
                        "Accountant": 14, "Digital Copywriter": 15, "Writer": 16,
                        "Web Content Manager": 17, "Therapist": 18, "Market Researcher": 19,
                        "Network Engineer": 20, "Design Engineer": 21, "Advertising": 22}

    major_count = len(major_indeces) - 1
    position_count = len(position_indeces) - 1

    def sigmoid(x):
        return 1 / (1 + numpy.exp(-x))

    # Algorithm
    a1 = numpy.zeros(major_count + position_count)
    a1 = numpy.insert(a1, 0, 1)
    if subject_info["college-major"] != "None":
        a1[major_indeces[subject_info["college-major"]]
           ] = degree_values[subject_info["college-degree"]]
    if subject_info["position"] != "None":
        a1[major_count + position_indeces[subject_info["position"]]
           ] = sigmoid(0.8 * subject_info["experience"] - 2)

    weights_file = open("./resources/weights.csv", "rb")
    z1 = numpy.loadtxt(weights_file, delimiter=",")
    weights_file.close()

    a2 = sigmoid(numpy.dot(a1, z1.T))

    def display_scores():
        print("Match Scores: ")
        temp0 = 0
        for i in position_indeces:
            if i != "None":
                print("\t{:30}: {:.2%}".format(i, a2[0, temp0]))
                temp0 = temp0 + 1

    # display_scores()

    return a2
