from playscript.conv import fountain

from conv.pdf import psc_to_pdf

def main():
    with open('example.fountain', encoding='utf-8-sig') as f:
        psc = fountain.psc_from_fountain(f.read())

    pdf = psc_to_pdf(psc)
    with open('out2.pdf', 'wb') as f:
        f.write(pdf.read())


if __name__ == '__main__':
    main()
