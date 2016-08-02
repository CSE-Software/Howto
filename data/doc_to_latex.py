TABLE_SIZE = 15.0
MIN_COL_SIZE = 2.0


# Delete non-ASCII character and modify the table
def cleanup(input_line):
    return input_line.decode('ascii', errors='ignore').replace("\\tabularnewline", "\\tabularnewline\\hline")


# Assign appropriate table width
def assign_table_width(ls):
    if MIN_COL_SIZE * len(ls) > TABLE_SIZE:
        return [round(TABLE_SIZE / len(ls), 2)] * len(ls)

    result = [0] * len(ls)
    value_index = sorted(enumerate(ls), key=lambda x: x[1])

    remain_table_size = TABLE_SIZE
    remain_sum = sum(ls)

    for index, value in value_index:
        weight = round(max(value*remain_table_size/remain_sum, MIN_COL_SIZE), 2)
        result[index] = weight
        remain_table_size -= weight
        remain_sum -= value
    return result


#  Modify latex
def fix_latex(input_filename, output_filename):
    with open(input_filename) as input_file:
        input_lines = input_file.readlines()

    flag_in_table = False
    count_column = 0
    num_column = None
    output_line = ""
    weight_ls = None
    weight_index = 0
    with open(output_filename, 'w') as output_file:
        for input_line in input_lines:
            if "begin{longtable}" in input_line:
                output_line = ""
                flag_in_table = True
                count_column = 0
                num_column = None
            elif "end{longtable}" in input_line:
                flag_in_table = False
                output_line += cleanup(input_line)

                spacing = "{"
                for width in assign_table_width(weight_ls):
                    spacing += "| m{" + str(width) + "cm} "
                spacing += "| }"
                output_line = "\\begin{longtable}" + spacing + "\n" + output_line
            elif flag_in_table:
                output_line += cleanup(input_line)
            else:
                output_line = cleanup(input_line)

            if flag_in_table:
                if num_column is None:
                    count_column += input_line.count("&")
                    if "\\tabularnewline" in input_line:
                        num_column = count_column + 1
                        weight_ls = [0] * num_column

                else:
                    reduce_line = input_line
                    for text in ["\\tabularnewline", "\\midrule\n", "\\endhead\n", "\\bottomrule\n"]:
                        reduce_line = reduce_line.replace(text, "")
                    for char in reduce_line:
                        if char == '&':
                            weight_index += 1
                        else:
                            weight_ls[weight_index] += 1
                    if "\\tabularnewline" in input_line:
                        weight_index = 0
            if not flag_in_table:
                output_file.write(output_line)


# main function
if __name__ == '__main__':
    fix_latex("ConfigurationHowToConfigureSoftware.tex", "output.tex")

