def copy_file(input_filename, output_filename):
    new_line = "tabularnewline"
    with open(input_filename) as input_file:
        lines = input_file.readlines()
    with open(output_filename, 'w') as output_file:
        #sc = special_charater
        nl = new_line
        for line in lines:
            #if sc in line:
            #    sc = ""
            if new_line in line:
                new_line += "\hline"
            output_file.write(line)



copy_file("ConfigurationHowToConfigureSoftware.tex", "output.txt")

