import csv
import json

#Eg: InfoCompare.exe -source=c:\1.csv -target=c:\2.csv -ratio=10 -ignore={} -fileType=Summary


def csv_check(file_path):
    if not file_path.lower().endswith('.csv'):
        return False
    
    with open(file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        temp = next(csv_reader)
        
        if temp is None:
            return False
        else:
            return True








def compsummary(source1, source2, ratio, ignore):

    #check that both are valid csv files
    if not csv_check(source2) or not csv_check(source2):
        return

    source1_dict = {}
    source2_dict = {}

    #read first file
    with open(source1, mode='r', newline='') as s1file:
        s1reader = csv.reader(s1file)

        #copy contents of first row --> for target file
        first_row = next(s1reader, None)

        if first_row == None:
            print("source 1 is empty")
            return
    
        #add to dictionary: key-company name, value-row contents
        for row in s1reader:
            if row: 
                temp = row[0]
                source1_dict[temp] = row[1:]


    #read second file
    with open(source2, mode='r', newline='') as s2file:
        s2reader = csv.reader(s2file)


        #add to dictionary: key-company name, value-row contents
        for row in s2reader:
            if row: 
                temp = row[0]
                source2_dict[temp] = row[1:]

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
                row.extend(["-"] * len(first_row[1:]))

            #if a company is in both sources, calculate ratio and compare with ratio limit
            if company in source1_dict and company in source2_dict:

                #store vals as floats
                source1_vals = list(map(float, source1_dict[company]))
                source2_vals = list(map(float, source2_dict[company]))


                for v1, v2 in zip(source1_vals, source2_vals):

                    #calculate diff
                    diff = abs((v2 - v1) / v1) * 100
                    if diff > ratio:
                        row.append("NAURRR")
                    else:
                        row.append("-")

            #handling companies that only appear in one source
            elif company in source1_dict:
                row.extend(["Only in Source 1"] * len(first_row[1:]))
            elif company in source2_dict:
                row.extend(["Only in Source 2"] * len(first_row[1:]))

            writer.writerow(row)




def main():

    print("\nPlease provide the necessary inputs in the following comma-separated format: \n\nPath to Source 1 File: eg: \"path/to/file.csv\"\nPath to Source 2 File: eg: \"path/to/file.csv\"\nRatio Limit: integer ranging from 0 to 100 \nCompanies to Ignore: eg [\"CompanyName 1\", \"CompanyName 2\"]\nType of Sources: \"Summary\" or \"Company\"\n")
    print("Format: source_1_file_name, source_2_file_name, ratio, companies_to_ignore, fileType\n")
    userinput = input("Enter the inputs: ")

    uinputs = userinput.split(',')

    source1 = uinputs[0].strip()
    source2 = uinputs[1].strip()
    ratio = float(uinputs[2].strip())
    try:
        ignore = json.loads(uinputs[3].strip().replace("'", "\""))
        if not isinstance(ignore, list):
            raise ValueError
    except:
        print(f"Error: Companies to Ignore is an invalid JSON array.")
        return
    
    
    fileType = uinputs[4].strip()


    print(source1)
    print(source2)
    print(ratio)
    print(ignore)
    print(fileType)

    if fileType == 'Summary':
        compsummary(source1, source2, ratio, ignore)



if __name__ == "__main__":


    main()

    #Enter the inputs: sample\total_summary(2024_03_production).csv, sample\total_summary(2024_02_production).csv, 10, ["Hi", "Hello"], Summary 