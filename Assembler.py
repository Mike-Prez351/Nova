import os
import re
import sys

class Assembler:
   def __init__(self):
       self.instructions = []
       self.data = []
       
   def _get_file_path(self, filename):
       script_dir = os.path.dirname(os.path.abspath(__file__))
       return os.path.join(script_dir, filename)
   
   def _read_assembly_file(self, filename):
       try:
           with open(self._get_file_path(filename), 'r') as file:
               return [line.strip() for line in file]
       except FileNotFoundError:
           sys.exit(f"Error: {filename} not found")
   
   def _write_output_file(self, filename, content):
       with open(self._get_file_path(filename), 'w') as file:
           file.write(content)
   
   def _parse_line(self, line):
       return [item for item in re.split('[ ,]+', line) if item]
   
   def _process_instruction(self, inst):
       if inst[0] == "ADD":
           opcode = 0
           shifts = (2, 4)
       elif inst[0] == "SUB":
           opcode = 64
           shifts = (2, 4)
       elif inst[0] == "LDR":
           opcode = 128
           shifts = (2, 0)
       elif inst[0] == "STR":
           opcode = 192
           shifts = (2, 0)
       else:
           sys.exit(f"Error: Invalid instruction {inst[0]}")
           
       target_reg = int(inst[1][1:])
       reg1 = int(inst[2][1:]) << shifts[0]
       reg2 = int(inst[3][1:]) << shifts[1] if len(inst) > 3 else 0
       
       return hex(opcode + target_reg + reg1 + reg2)[2:]  
   
   def _process_data(self, data):
       return hex(int(data[1]))[2:]
   
   def process_assembly(self):
       lines = self._read_assembly_file("assembly.txt")
       
       is_data_section = False
       text_section = []
       data_section = []
       
       for line in lines:
           if not line:
               continue
           if ".data" in line:
               is_data_section = True
           elif ".text" in line:
               is_data_section = False
           else:
               parsed_line = self._parse_line(line)
               if parsed_line:
                   if is_data_section:
                       data_section.append(parsed_line)
                   else:
                       text_section.append(parsed_line)
       
       instruction_hex = " ".join(self._process_instruction(inst) for inst in text_section)
       data_hex = " ".join(self._process_data(data) for data in data_section)
       
       self._write_output_file("instructions.txt", instruction_hex)
       self._write_output_file("data.txt", data_hex)
       
       print("Instructions:", instruction_hex)
       print("Data:", data_hex)

if __name__ == "__main__":
   assembler = Assembler()
   assembler.process_assembly()
