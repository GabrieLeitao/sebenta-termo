# 📘 Sebenta de Termodinâmica

Este texto enquadra-se na unidade curricular de Termodinâmica I de 2024/2025 de LEAer, LEAmb, LEMec, LEAN, no Instituto Superior Técnico. 

Inspirada no livro *Fundamentals of Engineering Thermodynamics* (Shapiro) \cite{shapiro}, esta sebenta é complementada com conteúdos lecionados em aula, organizados de forma a facilitar uma aprendizagem mais eficaz ao longo do período letivo. Inclui ainda exemplos resolvidos e notas históricas que ajudam a tornar os conceitos mais intuitivos.

Os ficheiros da sebenta estão disponíveis no repositório do [github.com/GabrieLeitao/sebenta-termo - GitHub](https://github.com/GabrieLeitao/sebenta-termo) para quem quiser contribuir com correções ou melhorias.

A termodinâmica é uma das disciplinas científicas mais fundamentais e abrangentes. O seu desenvolvimento ao longo dos séculos não apenas revolucionou a ciência, mas também transformou a tecnologia e a indústria, impulsionando a Revolução Industrial e moldando o mundo moderno.

---

## 📁 Organização do Projeto

A ordem dos capítulos segue de forma semelhante à dada nas aulas e à presente no Shapiro

```text
sebenta-termo/
├── graphs/
│   ├── g.py               # Código para gerar gráficos T-s Carnot, Rankine, Brayton, ideal, real, etc; graficos domo água T-v
│   └── gráficos gerados...
├── images/                # Contém outras imagens e gráficos do shapiro e de testes antigos úteis
│   └── ...
│
├── main.tex               # Main
│
├── fluidos.tex            # Introdução mecânica de fluidos para as equações da continuidade e Bernoulli, úteis para termodinâmica
├── intro.tex              # Introdução termodinâmica: conceitos base
├── primeiralei.tex        # Balanços de energia (sist. abertos e fechados) e definição de trabalho, calor e processo politrópico, entalpia
├── propriedades.tex       # Bifase da água, constante universal dos gases e modelo do gás ideal, calores específicos
├── segundalei.tex         # Formulações da segunda lei, introdução à entropia
├── entropia.tex           # Definição de entropia, Balanço de entropia, Geração de Entropia, Processos isentrópicos,...
├── ciclos.tex             # Tipos de ciclos, Eficiência de Carnot, Ciclos de Carnot, Rankine, Brayton
│
└── README.md
```

---

## 🧭 Normas de Contribuição

Para manter a organização e qualidade da sebenta:

1. Cada capítulo deve ser incluído separadamente com `\input{capituloX.tex}`.
2. Imagens e gráficos devem ser colocados apenas em `/images/` e os gráficos criados em python `/graphs/`.
3. Os gráficos devem ser vetoriais (`.pdf`) ou `.png` com resolução adequada.
4. Códigos de Python devem:
   - Estar na pasta `/graphs/`
   - Ter comentários

---

## ⚙️ Compilação da Sebenta

Podem usar compilação local com `TeX Live` ou Overleaf se não exceder o tempo de compilação.

### 🔧 Requisitos

- **LaTeX**: `TeX Live Full`
- **Pacotes:** `amsmath`, `amssymb`, `amsthm`, `cancel`, `graphicx`, `subcaption`, `float`, `hyperref`, `color`, `anysize`, `fancyhdr`, `titlesec`, `setspace`, `babel (portuguese)`, `fontenc (T1)`
- **Python 3** com: `matplotlib`, `numpy`, `CoolProp`

### 📦 Compilação manual (Linux/macOS)

O VScode trata de tudo, mas manualmente:

```bash
pdflatex main.tex
pdflatex main.tex
```

---

## 📌 Propostas de Continuidade

- Gráficos da eficiência do Ciclo de Brayton com a pressão;
- Gráficos do trabalho específico útil em função da razão de pressão (para encontrar razão de pressão ótima: 7.4.1 Trabalho máximo);
- Ciclos de Rankine com reaquecimento;
- Ciclos combinados;  
- Exercícios resolvidos relevantes 


## Contribuições

Gabriel Leitão, Gabriel Faria