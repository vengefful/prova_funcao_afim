import csv
from email.encoders import encode_noop
import os
import shutil
import subprocess
import re
import random

tema = 'Avaliação de Matemática - Bimestre II'
turma = '1i02'
parent_dir = r"C:\Users\eduin\Documents\Fernando\github\prova_funcao_afim"
provas_dir = os.path.join(parent_dir, 'provas')
logo = 'lima_castro.png'
latex_class = 'ufcdocument.cls'
latex_main = 'main.tex'

regex_ra = '@ra@'
regex_aluno = '@aluno@'
regex_turma = '@turma@'
regex_tema = '@tema@'

#getting alunos from turmas
with open(f"turmas/{turma}.csv", newline='', encoding="utf-8") as f:
    alunos = list(csv.reader(f))

aluno_dir = f"{alunos[0][1]} - {alunos[0][0]}"

#creating provas dir
if not os.path.isdir(provas_dir):
    os.mkdir(os.path.join(provas_dir))

#creating turmas dir
if not os.path.isdir(os.path.join(provas_dir, turma)):
    os.mkdir(os.path.join(provas_dir, turma))

#creating aluno dir
if not os.path.isdir(os.path.join(provas_dir, turma, aluno_dir)):
    os.mkdir(os.path.join(provas_dir, turma, aluno_dir))

#copying files from parent folder to aluno dir
if not os.path.exists(os.path.join(provas_dir, turma, aluno_dir, latex_main)):
    shutil.copy2(os.path.join(parent_dir, logo), os.path.join(provas_dir, turma, aluno_dir, logo))
    shutil.copy2(os.path.join(parent_dir, latex_main), os.path.join(provas_dir, turma, aluno_dir, latex_main))
    shutil.copy2(os.path.join(parent_dir, latex_class), os.path.join(provas_dir, turma, aluno_dir, latex_class))

with open(os.path.join(provas_dir, turma, aluno_dir, latex_main), 'r', encoding='utf-8') as f:
    main_tex = f.read()

#replace student info
main_tex = re.sub(regex_ra, alunos[0][0], main_tex)
main_tex = re.sub(regex_aluno, alunos[0][1], main_tex)
main_tex = re.sub(regex_turma, turma, main_tex)
main_tex = re.sub(regex_tema, tema, main_tex)

#question 1 - changing coeficient a and b of first function
#range of a [-10,10]
#range of b [-30,30]
regex_q1_function = "@q1-function@"

a = random.randrange(-10,10)
while(a == 0):
    a = random.randrange(-10,10)
b = random.randrange(-30,30)

if a < -1:
    signal_a = f"-{abs(a)}x"
elif a > 1:
    signal_a = f"{abs(a)}x"
elif a == 1:
    signal_a = f"x"
else:
    signal_a = f"-x"

if b < 0:
    signal_b = f"- {abs(b)}"
elif b > 0:
    signal_b = f"+ {abs(b)}"
else:
    signal_b = ''

dominio = []
contra_dominio = []
imagem = []
while len(dominio) < 5:
    x = random.randrange(-10,10)
    if not x in dominio:
        dominio.append(x)
        y = a*x + b
        imagem.append(y)
        contra_dominio.append(y)

while len(contra_dominio) < 10:
    x = random.randrange(-100, 100)
    if not x in contra_dominio:
        contra_dominio.append(x)

q1_function_string = f"f(x) = {signal_a} {signal_b}"
main_tex = re.sub(regex_q1_function, f"${q1_function_string}$", main_tex)

dominio.sort()
contra_dominio.sort()
imagem.sort()

#replacing conjunto A e B por Dominio e Contra Dominio
dominio_string = f"A = \{{"
for d in dominio:
    dominio_string += f"{d},"
dominio_string =  f"{dominio_string[:-1]}\}}"

contra_dominio_string = f"B = \{{"
for cd in contra_dominio:
    contra_dominio_string += f"{cd},"
contra_dominio_string =  f"{contra_dominio_string[:-1]}\}}"

main_tex = re.sub("@q1-A@", dominio_string, main_tex)
main_tex = re.sub("@q1-B@", contra_dominio_string, main_tex)
    


#question 2
#valor fixo: ]3,5]
#preco km: [0.5,1.50]
fixo = 3 + random.randrange(0,20)*0.1
preco_km = 0.5 + random.randrange(0,10)*0.1
resp = True
while resp:
    for i in range(50, 150):
        preco_b = i
        q2_resp_b = (preco_b - fixo)/preco_km
        if q2_resp_b.is_integer():
            resp = False
            break
    if resp:
        fixo = 3 + random.randrange(0,20)*0.1
        preco_km = 0.5 + random.randrange(0,10)*0.1

q2_function_string = f"P(x) = {preco_km:.2f}x + {abs(fixo):.2f}"

#letra c questao 2
km = random.randrange(10,30)
preco_c = preco_km * km + fixo

main_tex = re.sub("@q2-fixo@", f"${fixo:.2f}$", main_tex)
main_tex = re.sub("@q2-preco-km@", f"${preco_km:.2f}$", main_tex)
main_tex = re.sub("@q2-preco-b@", f"${preco_b:.2f}$", main_tex)
main_tex = re.sub("@q2-km-c@", f"${km}$", main_tex)

#question 3
q3_function = []
for i in range(3):
    a = random.randrange(-3,3)
    while(a == 0):
        a = random.randrange(-3,3)
    b = random.randrange(-3,3)

    if a < -1:
        signal_a = f"-{abs(a)}x"
    elif a > 1:
        signal_a = f"{abs(a)}x"
    elif a == 1:
        signal_a = f"x"
    else:
        signal_a = f"-x"

    if b < 0:
        signal_b = f"- {abs(b)}"
    elif b > 0:
        signal_b = f"+ {abs(b)}"
    else:
        signal_b = ''
    q3_function.append(f"f(x) = {signal_a} {signal_b}")

main_tex = re.sub("@q3-a@", f"${q3_function[0]}$", main_tex)
main_tex = re.sub("@q3-b@", f"${q3_function[1]}$", main_tex)
main_tex = re.sub("@q3-c@", f"${q3_function[2]}$", main_tex)

#question 4
a = random.randrange(-5,5)*2
while(a == 0):
    a = random.randrange(-5,5)*2
b = random.randrange(-10,10)*2

if a < -1:
    signal_a = f"-{abs(a)}x"
elif a > 1:
    signal_a = f"{abs(a)}x"
elif a == 1:
    signal_a = f"x"
else:
    signal_a = f"-x"

if b < 0:
    signal_b = f"- {abs(b)}"
elif b > 0:
    signal_b = f"+ {abs(b)}"
else:
    signal_b = ''

q4_function = (f"f(x) = {signal_a} {signal_b}")
letra_4a = "decrescente" if a < 0 else "crescente"
letra_4b = b
letra_4c = -b/a

main_tex = re.sub("@q4-function@", f"${q4_function}$", main_tex)

#question 5
fixo_a = random.randrange(10,20)*5
fixo_b = fixo_a + random.randrange(5,20)*5
km_a = random.randrange(0,6)*0.5 + 2
km_b = km_a - 0.5
x = (fixo_b - fixo_a)/(km_a - km_b)

main_tex = re.sub("@q5-fixo-a@", f"${fixo_a:.2f}$", main_tex)
main_tex = re.sub("@q5-fixo-b@", f"${fixo_b:.2f}$", main_tex)
main_tex = re.sub("@q5-km-a@", f"${km_a:.2f}$", main_tex)
main_tex = re.sub("@q5-km-b@", f"${km_b:.2f}$", main_tex)

#saving respostas
with open(os.path.join(provas_dir, turma, aluno_dir, 'respostas.txt'), 'w') as f:
    f.write('questao 1\n')
    f.write(f"funcao: {q1_function_string}\n")
    f.write(f"dominio: {dominio}\n")
    f.write(f"contra dominio: {contra_dominio}\n")
    f.write(f"imagem {imagem}\n")
    f.write('questao 2\n')
    f.write(f"letra a: {q2_function_string}\n")
    f.write(f"letra b: {q2_resp_b} quilometros\n")
    f.write(f"letra c: {preco_c:.2f}\n")
    f.write('questao 4\n')
    f.write(f"letra a: {letra_4a}\n")
    f.write(f"letra b: {letra_4b}\n")
    f.write(f"letra c: {letra_4c}\n")
    f.write('questao 5\n')
    f.write(f"resposta: {x} quilometros\n")

#saving main.tex
with open(os.path.join(provas_dir, turma, aluno_dir, latex_main), 'w', encoding='utf-8') as f:
    f.write(main_tex)


#call pdflatex - creating pdf of aluno
subprocess.call(['pdflatex.exe', os.path.join(provas_dir, turma, aluno_dir, latex_main), f"--output-directory={os.path.join(provas_dir, turma, aluno_dir)}", '--quiet'])