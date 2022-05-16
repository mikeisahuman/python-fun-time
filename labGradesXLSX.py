## labGrades
## by Mike Phillips, 11/14/2017
##
## for importing gradebooks from Excel and calculating weighted averages for overall lab grades,
## both at end of term (after final) and part-way through the term (e.g. after a mid-term)
##

import os
import numpy as np
import matplotlib.pyplot as plt
import xlrd

plt.close()         # close any open figures before beginning

###     EDIT THIS SECTION:  FILE/PATH NAMES     ###
numStudents = 19
# location(s) of gradebook(s)
term = "2017 fall"
classno = "1792"
gradeDir = os.path.join("/Users/HamburgerTime/Documents/CNM stuffs", term, classno, "grading")
shorthands = []                                 # empty list for shorthands (dictionary use)
bookCount = 0                                   # counter for the number of gradebook files
labName = "lab_grades (simple).xlsx"            # lab grades filename
shorthands.append("lab")                        # add shorthand name for the workbook
bookCount += 1                                  # increase the count
# types of 'labs' (entries in the lab gradebook)
LABTYPES = ("LAB", "PART", "MID-TERM", "FINAL")
WEIGHTS = {"LAB":0.60, "PART":0.10, "MID-TERM":0.15, "FINAL":0.15}
PERC_COMPLETE = 1            # percent of the class considered complete [here: final is not yet taken]
### ### ### ### ### ### ### ### ### ### ### ### ###


# load the excel workbooks as objects
fNames = (labName,)           # list of filenames
paths = []                                      # empty list for pathnames
books = {}                                      # empty dictionary for excel workbooks
for bk in range(bookCount):
    paths.append( os.path.join(gradeDir, fNames[bk]) )    # pathname added
    books.update( {shorthands[bk] : xlrd.open_workbook(paths[-1])} )       # gradebook added

#print("\n\n",paths,"\n"*8)

###

# read information line-by-line (row-by-row) for each file, dropping any assignments/total points of each type
scores = {}                     # dictionary for all scores (by student name)
students = []                   # empty list for student names (full names)
stu_lens = []                   # list to track the length of student names (for table output)

aBook = books[shorthands[0]]
aSheet = aBook.sheet_by_index(0)
line1 = aSheet.row_values(0)     # labels
Fname_i = line1.index("First Name")   # index of the column for first names
Lname_i = line1.index("Last Name")    # index for last names
PART_i = line1.index("PARTICIPATION")   # participation index (column)
MT_i = line1.index("MID-TERM")          # mid-term index
FINAL_i = line1.index("FINAL")          # final index
LABIND = {"PART":PART_i, "MID-TERM":MT_i, "FINAL":FINAL_i}  # dictionary of column indices

line2 = aSheet.row_values(1)     # total points possible [participation & exams]

for st in range(numStudents):
    line = aSheet.row_values(2 + st)        # data (student name followed by scores, eventually totals)
    Fname, Lname = line[Fname_i], line[Lname_i] # names of current student
    fullname = " ".join([Fname, Lname])     # full name of current student
    if fullname not in students:
        students.append(fullname)
        stu_lens.append(len(fullname))
    
    TypeScores = {}                 # dictionary for scores (by grade type) for the lab gradebook
    for typ in LABTYPES:
        maxpts = 0                              # initialize maximum points for the student
        stpts = 0                               # initialize points of the given type for the student
        minscore = 1                            # initialize percentage to check minimum score
        if typ == "LAB":
            for i in range( (Lname_i + 1), FINAL_i):
                if typ in line1[i].upper():
                    cell = line[i]
                    if type(cell) != str:
                        maxpts += 1                 # max points always 1 for labs
                        stpts += cell               # add actual score to total student points
                        if cell < minscore:
                            minscore = cell         # track the minimum score
#                            min_i = i               # track the index of the minimum score
            aScore = (stpts - minscore)/(maxpts - 1)
            TypeScores.update({ typ: aScore })    # add student's lab report score to the dictionary
        else:
            ind = LABIND[typ]
            cell = line[ind]
            if type(cell) != str:
                maxpts = line2[ind]
                stpts = line[ind]
                aScore = stpts/maxpts
                TypeScores.update({ typ: aScore })    # add student's other scores to the dictionary
        
    scores.update({fullname: TypeScores}) # add the scores of all students to the big dictionary

###

#print(scores)

# combine all the scores to get overall grades
overall = {}
max_stu_len = max(stu_lens)
for stu in students:
    overallGrade = 0
    for typ in scores[stu]:
        student_score = scores[stu][typ]
        overallGrade += WEIGHTS[typ] * student_score
    overallGrade *= 1/PERC_COMPLETE             # rescale (for getting grades part-way through the term)
    overall.update({ stu: overallGrade })

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

def gradePlot(title, grades, pos, bins=8, size="23"):
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
for typ in LABTYPES:
    plot_pos += 1
    gds = []
    if typ in list(scores.values())[0]:
        for stu in students:
            if typ in scores[stu]:
                gds.append(scores[stu][typ])    
        title = typ
        grades = np.array(gds)
        gradePlot(title, grades, plot_pos)
#    
plt.show()
# >>                    << #



# clear out modules
del xlrd, plt, np, os
