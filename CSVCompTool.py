import csv

#checks validity of path to csv file
def csv_check(file_path):
    #check ending of file path
    if not file_path.lower().endswith('.csv'):
        return False
    
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        temp = next(csv_reader)
        
        if temp is None:
            return False
        else:
            return True

#removes blank or whitespace elements from an array
def remove_blanks(inputarray):
    return [i.strip() for i in inputarray if i.strip()]



def compSummary(source1, source2, ratio, ignore):

    #check that both are valid csv files
    if not csv_check(source2) or not csv_check(source2):
        print("One or both source files are invalid.\n")
        return

    source1_dict = {}
    source2_dict = {}

    #read first file
    with open(source1, mode='r', newline='') as s1file:
        s1reader = csv.reader(s1file)

        #copy contents of first row --> for target file
        first_row = next(s1reader, None)

        if first_row == None:
            print("Source 1 is empty\n")
            return
    
        #add to dictionary: key-company name, value-row contents
        for row in s1reader:
            if row: 
                temp = row[0]
                source1_dict[temp] = remove_blanks(row[1:])


    #read second file
    with open(source2, mode='r', newline='') as s2file:
        s2reader = csv.reader(s2file)
        if s2reader == None:
            print("Source 2 is empty\n")
            return

        #add to dictionary: key-company name, value-row contents
        for row in s2reader:
            if row: 
                temp = row[0]
                source2_dict[temp] = remove_blanks(row[1:])

    #create a target file
    with open('target.csv', mode='w', newline='') as targetfile:
        writer = csv.writer(targetfile)

        #write first row
        writer.writerow(first_row)

        #save all companies
        all_companies = set(source1_dict.keys()).union(set(source2_dict.keys()))

        #iterate through all companies, write to target
        for company in all_companies:
            row = [company]

            #if company in ignore, it's passed
            if company in ignore:
                row.extend(["I"] * len(first_row[1:]))

            #if a company is in both sources, calculate ratio and compare with ratio limit
            if company in source1_dict and company in source2_dict:

                #store vals as floats
                source1_vals = list(map(float, source1_dict[company]))
                source2_vals = list(map(float, source2_dict[company]))


                for v1, v2 in zip(source1_vals, source2_vals):

                    #calculate diff
                    if v1 == 0 and v2 == 0: 
                        row.append("-")
                    else: 
                        if v1 == 0:
                            diff = abs(v2) #if first month count = 0, diff = second month count
                        else:  
                            diff = abs((v2 - v1) / v1) * 100
                        
                        if diff > ratio:
                            row.append("X")
                        else:
                            row.append("-")

            #handling companies that only appear in one source
            elif company in source1_dict:
                row.extend(["1"] * len(first_row[1:]))
            elif company in source2_dict:
                row.extend(["2"] * len(first_row[1:]))

            writer.writerow(row)




def main():

    print("\nSee User Manual for input and format\n")
    userinput = input("Type here: ")

    uinputs = userinput.split(';')

    if len(uinputs) != 5:
        print(len(uinputs))
        print("Incorrect number of inputs. Please enter the inputs in the specified format.")
        return

    source1 = uinputs[0].strip()
    source2 = uinputs[1].strip()
    ratio = float(uinputs[2].strip())

    ignore = uinputs[3].strip()

    if ignore.startswith('[') and ignore.endswith(']'):
        ignore = ignore[1:-1]
        ignore = [c.strip() for c in ignore.split(',')]
    else:
        print("Companies to ignore should be in the format [Company A, Company B].")
        return
    
    fileType = uinputs[4].strip()

    if fileType == 'Summary':
        compSummary(source1, source2, ratio, ignore)
    else:
        return
    
    print("\nSee target.csv to view results\n")



if __name__ == "__main__":


    main()


#IGNORE THIS
#/Users/gracefayeyang/Desktop/infocomptool/sample/total_summary(2024_02_production).csv; /Users/gracefayeyang/Desktop/infocomptool/sample/total_summary(2024_03_production).csv; 10; [Hi, Hello]; Summary 

