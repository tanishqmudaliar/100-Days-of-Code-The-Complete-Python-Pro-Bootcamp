student_scores = [150, 142, 185, 120, 171, 184, 149, 24, 59, 68, 199, 78, 65, 89, 86, 55, 91, 64, 89]
exam_scores = [8, 65, 89, 86, 55, 91, 64, 89]
sumOne,sumTwo = 0,0
for score in exam_scores:
    if score > sumOne:
        sumOne = score
    if score < sumTwo or sumTwo == 0:
        sumTwo = score
print(sumOne, sumTwo)
