import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

# Função para converter XML para KML
def xml_para_kml(xml_string):
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    
    for placemark in root.findall('.//kml:Placemark', namespaces):
        name = placemark.find('kml:name', namespaces)
        coordinates = placemark.find('.//kml:coordinates', namespaces)
        
        # Verifica se a tag name e coordinates não são None
        if name is not None and coordinates is not None:
            name_text = name.text.strip() if name.text else ""
            coordinates_text = coordinates.text.strip() if coordinates.text else ""
            
            kml_content += f'  <Placemark>\n'
            kml_content += f'    <name>{name_text}</name>\n'
            kml_content += f'    <Polygon>\n'
            kml_content += f'      <outerBoundaryIs>\n'
            kml_content += f'        <LinearRing>\n'
            kml_content += f'          <coordinates>{coordinates_text}</coordinates>\n'
            kml_content += f'        </LinearRing>\n'
            kml_content += f'      </outerBoundaryIs>\n'
            kml_content += f'    </Polygon>\n'
            kml_content += f'  </Placemark>\n'
        else:
            # Se algum valor não for encontrado, logar para depuração
            print(f"Erro ao processar Placemark: {placemark}")
    
    kml_content += '</Document>\n'
    kml_content += '</kml>\n'
    
    return kml_content

# Função para abrir o arquivo XML e gerar o KML
def escolher_arquivo():
    xml_file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
    if xml_file_path:
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                xml_string = file.read()
                kml_result = xml_para_kml(xml_string)
                
                # Salvar o KML em um arquivo
                kml_file_path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML Files", "*.kml")])
                if kml_file_path:
                    with open(kml_file_path, 'w', encoding='utf-8') as kml_file:
                        kml_file.write(kml_result)
                    messagebox.showinfo("Sucesso", f"KML gerado com sucesso!\nSalvo em: {kml_file_path}")
                else:
                    messagebox.showwarning("Aviso", "Você não escolheu onde salvar o KML.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao processar o arquivo XML: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo XML foi selecionado.")

# Criação da interface gráfica
root = tk.Tk()
root.title("Conversor XML para KML")

# Definir tamanho e layout da janela
root.geometry("400x200")

# Label de instrução
label = tk.Label(root, text="Escolha um arquivo XML para gerar o KML", padx=20, pady=20)
label.pack()

# Botão para escolher o arquivo XML e gerar o KML
botao_gerar_kml = tk.Button(root, text="Escolher arquivo XML", command=escolher_arquivo, padx=20, pady=10)
botao_gerar_kml.pack()

# Adicionando o nome no canto inferior direito
nome_label = tk.Label(root, text="Filipe Gabriel - Rouxinol", font=("Arial", 8), anchor="e")
nome_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

# Rodar a interface
root.mainloop()
