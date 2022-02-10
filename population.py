from registered_courses import *
from time_table import *
from student_clashes import *
import random
from numpy import random as rn

crossover_probability = round(rn.uniform(low=0.3, high=1.0), 1)
mutation_probability = round(rn.uniform(low=0.0, high=0.5), 1)

class Population:
    def __init__(self, number, fitness, chromosome, t_sections):
        self.number = number
        self.fitness = fitness
        self.chromosome = chromosome
        self.t_sections = t_sections

    def __repr__(self):
        return ('(Population Number: {0}\Student Clashes: {1}\nChromosome: \n{2})\n'.format(self.number, self.fitness,
                                                                                     self.chromosome))
    



def initial_population():
    
    timetables = [] 

    for z in range(100): # 100 Solutions will be generated. 
        timetable = [] 
        generated_timetable = {} 
        t_sections = {}
        #timetables.append(generated_timetable)
        section_slots = {}
        for reg_course in reg_data:
            i = sections.sections_data[reg_course.section_id].name[:5] # Getting Section Name. 
            # Appending to Timetable Chromosome
            prev_day = 0
            if (i) not in t_sections.keys():
                t_sections[i] = []
                section_slots[i] = []
                generated_timetable[i] = [["" for i in range(5)] for j in range(5)]

            if courses.courses_data[reg_course.course_id].type == "Lab":
                day = random.randint(1, 4)
                slot = random.randint(1, 4)
                count = 0
                while ([day, slot] in section_slots[i] or [day, slot+1] in section_slots[i]):
                    day = random.randint(1, 4)
                    slot = random.randint(1, 4)
                    if (count > 500):
                        break
                    count = count + 1
                section_slots[i].append([day, slot])
                section_slots[i].append([day, slot+1])
                slots = []
                slots.append(Slot(day, slot))
                slots.append(Slot(day, slot+1))
                lecture = Timetable(reg_course.id, slots)
            else:
                slots = []
                for x in range(2):
                    day = random.randint(1, 5)
                    slot = random.randint(1, 5)
                    count = 0
                    while ([day, slot] in section_slots[i] or day == prev_day):
                        day = random.randint(1, 5)
                        slot = random.randint(1, 5)
                        if (count > 500):
                            break
                        count = count + 1
                    prev_day = day
                    section_slots[i].append([day, slot])
                    slots.append(Slot(day, slot))
                lecture = Timetable(reg_course.id, slots)
            timetable.append(lecture)
            t_sections[i].append(reg_course.id)
        clash_count = get_student_clashes(timetable, reg_data)
        population = Population(z, clash_count, timetable, t_sections)
        timetables.append(population)
        #print(timetables)
    return timetables
 

# PARENT SELECTION 
# Roulette Wheel Selection 
def parent_selection(population):
    parents = []
    total_value = 0  # Total Fitness

    for individual in population:
        total_value += individual.fitness
    # Applying Roulette Wheel
    # Check Total sum value of fittest individuals
    while len(parents) < 100:
        # Finding  probability of all chromosomes
        probability_arr = []
        for i in range(0, len(population)):
            s = (round((population[i].fitness / total_value), 2), i)
            probability_arr.append(s)

        # sorting the array having the probabilities
        probability_arr.sort(key=lambda val: val[0], reverse=True)
        # Making proper probability pie chart array
        temp_prob_arr = []
        check_temp = 0
        for i in range(0, len(population)):
            prob, ind = probability_arr[i]
            temp_prob_arr.append((prob + check_temp, ind))
            check_temp += prob
        # deciding the chromosome by random number generation and probability
        random_no = round(random.uniform(0, 1), 2)
        for i in range(0, len(temp_prob_arr)):
            prob, ind = temp_prob_arr[i]
            if random_no <= prob:
                parents.append(population[ind])
                break
    return parents



def find_fittest(population):
    population.sort(key=lambda val: val.fitness, reverse=False)

    return population[0],population[1]


def apply_crossover(population, length, chromosome_length):
    j = 0
    crossover_population = []
    for i in range(100):
        if random.randint(0, 100) <= crossover_probability * 100:

            # Randomly selecting two chromosomes
            first = random.randint(0, length)
            second = random.randint(0, length)
            # first, second = find_fittest(population)

            crossovered_timetable1 = [] 
            crossovered_timetable2 = []
            
            for k in range(chromosome_length):
                #print("For K: " + str(k))
                if k <= int(chromosome_length / 2):
                    #print("First K: " + str(k))
                    crossovered_timetable1.append(population[first].chromosome[k])
                    crossovered_timetable2.append(population[second].chromosome[k])
                else: 
                    #print("Second K: " + str(k))
                    crossovered_timetable1.append(population[second].chromosome[k])
                    crossovered_timetable2.append(population[first].chromosome[k])

            # new_crossovered_exams1 = apply_mutation(crossovered_exams1.copy())
            # new_crossovered_exams2 = apply_mutation(crossovered_exams2.copy())

            clash_count = get_student_clashes(crossovered_timetable1, reg_data)
            pops = Population(j, clash_count, crossovered_timetable1)
            crossover_population.append(pops)

            clash_count = get_student_clashes(crossovered_timetable2, reg_data)
            pops = Population(j + 1, clash_count, crossovered_timetable2)
            crossover_population.append(pops)

            # fitness = calculateFitness(new_crossovered_exams1, courses_data, students_data, teachers_data)
            # x, y = fitness
            # fitness = (x, (100 - y))
            # crossover_population.append(Population(j, fitness, crossovered_exams1))

            # fitness = calculateFitness(new_crossovered_exams2, courses_data, students_data, teachers_data)
            # x, y = fitness
            # fitness = (x, (100 - y))
            # crossover_population.append(Population(j + 1, fitness, crossovered_exams2))

            j += 2

    return crossover_population


"""-------------------------------------Mutation Function--------------------------------"""


# Apply Mutation on chromosomes , given Mutation probability
def apply_mutation(chromosome):
    # Randomly switch values(Day, Time) of a chromosome
    if random.randint(0, 100) <= mutation_probability * 100:
        genes = random.randint(0, 3)
        for i in range(genes):
            gene = random.randint(0, len(chromosome) - 1)
            temp = random.randint(0, len(days_data) - 1)

            # Date Switch
            chromosome[gene].day = days_data[temp].day
            chromosome[gene].binary_value[4] = days_data[temp].binary_val

            # Time Switch
            temp = random.randint(0, len(times_data) - 1)
            chromosome[gene].time = times_data[temp].time
            chromosome[gene].binary_value[3] = times_data[temp].binary_val

            # Room Switch
            temp = random.randint(0, len(rooms_data) - 1)
            while rooms_data[temp].num in chromosome[gene].room:
                temp = random.randint(0, len(rooms_data) - 1)

            temp1 = random.randint(0, len(chromosome[gene].room) - 1)
            chromosome[gene].room[temp1] = rooms_data[temp].num
            chromosome[gene].binary_value[1][temp1] = rooms_data[temp].binary_val

    return chromosome



def genetic_algo():
    best_solution = None
    max_iter = 50
    population = initial_population()
    count = 0
    regen = 1
    population.sort(key = lambda x: x.fitness, reverse=False)
    print()
    f = open("Folder/population 0.txt", "w")
    f.write(str(population))
    for i in range(max_iter):
        print("Generation " + str(i) + " going on.....")
        population1 = apply_crossover(population, (len(population) - 1), (len(population[0].chromosome)))
        population = parent_selection(population1.copy())
        temp_best, _ = find_fittest(population.copy())
        if best_solution is None:
            best_solution = temp_best 
        elif temp_best.fitness < best_solution.fitness:
            best_solution = temp_best 
        
        population.sort(key = lambda x: x.fitness, reverse=False)
        f = open("Folder/population " + str(i+1) + ".txt", "w")
        f.write(str(population))

        print("Generation " + str(i) + " Done!.....")
        print("Best Solution Fitness: " + str(best_solution.fitness))


        count += 1 

genetic_algo()

# print(pop[0].chromosome[2])
# print(pop[0])
# print("\n\n---------------\n\n")
# print(pop[0].chromosome)
# print("\n\n----------------\n\n")
# print(len(pop[0].chromosome))
#f = open("damn_man.txt", "w")
#f.write(str(pop))
#print("First Done")
#pop = parent_selection(pop)
# f = open("Folder/damn_man.txt", "w")
#pop.sort(key=lambda x: x.fitness, reverse=False)
#pop.sort(key=lambda x: x.fitness, reverse=False)
# f = open("damn_man.txt", "w")
# f.write(str(pop))