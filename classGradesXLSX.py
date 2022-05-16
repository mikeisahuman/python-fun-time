## classGrades
## by Mike Phillips, 11/7/2017
##
## for importing gradebooks from Excel and calculating weighted averages for overall grades,
## both at end of term (after final) and part-way through the term (e.g. after a mid-term)
##

import os
import numpy as np
import matplotlib.pyplot as plt
import xlrd

plt.close()         # close any open figures before beginning

###     EDIT THIS SECTION:  FILE/PATH NAMES     ###
numStudents = 26        # total students (including those who dropped -- full gradebooks)
# location(s) of gradebook(s)
term = "2017 fall"
classno = "1710"
gradeDir = os.path.join("/Users/HamburgerTime/Documents/CNM stuffs", term, classno, "grading")
shorthands = []                                 # empty list for shorthands (dictionary use)
bookCount = 0                                   # counter for the number of gradebook files
partName = "participation grading (simple).xlsx"         # participation grades filename
shorthands.append("part")                       # add shorthand name for the workbook
bookCount += 1                                  # increase the count
hwName = "problem set grading (simple).xlsx"             # homework grades filename
shorthands.append("hw")
bookCount += 1
examName = "exam grading (simple).xlsx"                  # exam grades filename
shorthands.append("exam")
bookCount += 1
# types of 'exams' (entries in the exam book)
EXAMTYPES = ("MT1", "MT2", "challenge 1", "challenge 2", "FINAL")
WEIGHTS = {"part":0.05, "hw":0.45,
           "MT1":0.18, "MT2":0.12, "challenge 1":0.025, "challenge 2":0.025, "FINAL":0.20}
PERC_COMPLETE = 1            # percent of the class considered complete [here: final is not yet taken]
### ### ### ### ### ### ### ### ### ### ### ### ###


# load the excel workbooks as objects
fNames = (partName, hwName, examName)           # list of filenames
paths = []                                      # empty list for pathnames
books = {}                                      # empty dictionary for excel workbooks
for bk in range(bookCount):
    paths.append( os.path.join(gradeDir, fNames[bk]) )    # pathname added
    books.update( {shorthands[bk] : xlrd.open_workbook(paths[-1])} )       # gradebook added

#print("\n\n",paths,"\n"*8)

###

# read information line-by-line (row-by-row) for each file, dropping any assignments/total points of each type
scores = {}                     # dictionary for all scores
students = []                   # empty list for student names (full names)
stu_lens = []                   # list to track the length of student names (for table output)

for aBookName in shorthands:
    aBook = books[aBookName]
    aSheet = aBook.sheet_by_index(0)
    line1 = aSheet.row_values(0)     # labels
    Fname_i = line1.index("First Name")   # index of the column for first names
    Lname_i = line1.index("Last Name")    # index for last names
    if aBookName in ["part", "hw"]:
        total_i = line1.index("TOTALS")   # index of the column "TOTALS"
    else:
        total_i = len(line1) - 1
    line2 = aSheet.row_values(1)     # dates (converted to integers)[part], or total points possible [hw/exam]

    aBookScores = {}                 # dictionary for scores (by student name) for the current book
    for st in range(numStudents):
        line = aSheet.row_values(2 + st)        # data (student name followed by scores, eventually totals)
        Fname, Lname = line[Fname_i], line[Lname_i] # names of current student
        fullname = " ".join([Fname, Lname])     # full name of current student
        if fullname not in students:
            students.append(fullname)
            stu_lens.append(len(fullname))
        maxpts = 0                              # initialize maximum points for the student
        minscore = 1                            # initialize percentage to check minimum score
        if aBookName in ("part", "hw"):
            for i in range((Lname_i + 1),total_i):    # loop over earned points
                cell = line[i]
                if type(cell) != str:               # check for number in cell (blank cells are not counted)
                    if aBookName == "part":
                        maxpts += 1                 # each participation item is worth 1 point
                    elif aBookName == "hw":
                        hwmax = line2[i]
                        if cell/hwmax < minscore:
                            minscore = cell/hwmax   # track the minimum hw score (percent)
                            min_i = i               # track the index (column) so that the entry is dropped
                        maxpts += hwmax
        else:
            examScores = {}                     # empty dictionary for various exam scores
            for examType in EXAMTYPES:
                exam_i = line1.index(examType)
                if type(line[exam_i]) != str:      # check that the column has grades (max points)
                    maxpts = line2[exam_i]
                    curved = "-".join([examType, "curved"])
                    if (curved in line1) and (type(line2[ line1.index(curved) ]) != str):
                        exam_i = line1.index(curved)    # shift to curved scores, if applicable
                    if type(line[exam_i]) != str:
                        examScore = line[exam_i]/maxpts     # exam scores are calculated simply at this point
                    else:
                        examScore = 0
                    examScores.update({ examType: examScore })
            if ("MT1" in examScores) and ("MT2" in examScores) and (examScores["MT1"] < examScores["MT2"]):
                # swap scores if needed (force MT1 > MT2)
                examScores["MT1"], examScores["MT2"] = examScores["MT2"], examScores["MT1"]
            aScore = examScores
        if aBookName == "part":
            aScore = line[total_i]/maxpts       # overall score (decimal < 1)
        elif aBookName == "hw":
            if (maxpts - line2[min_i]) > 0:
                aScore = (line[total_i] - line[min_i])/(maxpts - line2[min_i])      # homework score, drop lowest
            else:
                aScore = 0
        aBookScores.update({ fullname: aScore })    # add student's score to the dictionary
        
    scores.update({aBookName: aBookScores}) # add the scores of all students to the big dictionary

###

#print(scores)

# combine all the scores to get overall grades
overall = {}
max_stu_len = max(stu_lens)
for stu in students:
    overallGrade = 0
    for aBookName in shorthands:
        student_score = scores[aBookName][stu]
        if aBookName == "exam":
            for ex in EXAMTYPES:
                if ex in student_score:
                    overallGrade += WEIGHTS[ex] * student_score[ex]
        else:
            overallGrade += WEIGHTS[aBookName] * student_score
    overallGrade *= 1/PERC_COMPLETE             # rescale (for getting grades part-way through the term)
    overall.update({ stu: overallGrade })

##    if "saad" in stu.lower():
##        print(("\t" + "{:^" + str(max_stu_len) + "}" + "\t" + "{:2.2f}").format(stu, round(overallGrade*100,2)) )
    #print("\n\t\t",stu,"\t\t",round(overallGrade*100,4))       # print a crude table of names & grades
    #print(("\t" + "{:^" + str(max_stu_len) + "}" + "\t" + "{:2.2f}").format(stu, round(overallGrade*100,2)) )
    print(round(overallGrade*100,2))            # print grades vertically to ease copying
                                                #   (preserves original ordering of students)

#print(overall)                     # print the raw dictionary of grades


### ### ### ### ### ### ### ### ### ### ### ### ###

# now we may want to do some analysis the grades, either overall or by individual pieces
SIZE = 8            # figure size
BG = 'w'            # background color code
hist_STY = 'b'      # histogram style color code
mn_STY = 'g-'       # style code for mean lines
std_STY = 'r--'     # style code for std. dev. lines

# >> overall << #
grades0 = np.array(list(overall.values()))
fig0 = plt.figure("Grades : %i students" % numStudents, (int(SIZE*(1.5)), SIZE), facecolor = BG)
ax0 = fig0.add_subplot(231, facecolor = BG)#, aspect = "equal")
ax0.set_title("Overall")
ax0.set_xlim( 0.0, 1.0 )
# put histogram of grades
ax0.hist(grades0, bins=8, bottom=0, color=hist_STY, rwidth=0.8 )
ylim0 = ax0.get_ylim()
# add lines for mean and standard deviation
mean0 = np.mean(grades0)
std0 = np.std(grades0)
ax0.plot(np.array([mean0, mean0]), np.array([0,numStudents]), mn_STY)
ax0.plot(np.array(2*[mean0 - std0]), np.array([0,numStudents]), std_STY)
ax0.plot(np.array(2*[mean0 + std0]), np.array([0,numStudents]), std_STY)

ax0.set_ylim(ylim0)
#plt.show()
# >>         << #

def gradePlot(title, grades, pos, size="23"):
    ax = fig0.add_subplot(int("23"+str(pos)), facecolor = BG)#, aspect = "equal")
    ax.set_title(title.upper())
    ax.set_xlim( 0.0, 1.0 )
    # put histogram of grades
    ax.hist(grades, bins=8, bottom=0, color=hist_STY, rwidth=0.8 )
    ylim = ax.get_ylim()
    # add lines for mean and standard deviation
    mean = np.mean(grades)
    std = np.std(grades)
    ax.plot(np.array([mean, mean]), np.array([0,numStudents]), mn_STY)
    ax.plot(np.array(2*[mean - std]), np.array([0,numStudents]), std_STY)
    ax.plot(np.array(2*[mean + std]), np.array([0,numStudents]), std_STY)
    #
    ax.set_ylim(ylim)

# >> by assignment type << #
plot_pos = 1
for aBookName in shorthands:
    plot_pos += 1
    if aBookName != "exam":
        title = aBookName
        grades = np.array(list(scores[aBookName].values()))
        gradePlot(title, grades, plot_pos)
    else:
        for ex in EXAMTYPES:
            if ex not in ("challenge 1", "challenge 2"):
                title = ex
                gds = []
                for st in students:
                    st_scores = scores[aBookName][st]
                    if ex in st_scores:
                        gds.append(st_scores[ex])
                grades = np.array(gds)
                gradePlot(title, grades, plot_pos)
                plot_pos += 1
    #    
#    
plt.show()
# >>                    << #


#plt.close()

# clear out modules
del xlrd, plt, np, os
