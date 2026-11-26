"""
Cria o documento de referência (estilos) usado pelo pandoc para gerar o relatório final em DOCX.
Parte do reference.docx padrão do pandoc e troca estilos, margens e rodapé:
Arial 12, espaçamento 1,5, texto justificado com recuo de 1,25 cm, margens 3/2 cm (ABNT NBR 14724),
títulos em preto, tabelas com bordas finas, legendas e fontes em 10 pt e número da página no rodapé
(sem número na capa).
"""
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

LINHA_15 = '<w:spacing w:before="0" w:after="120" w:line="360" w:lineRule="auto"/>'
LINHA_1 = '<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'


def _rpr(tam=24, negrito=False, italico=False, caps=False, cor="000000", fonte="Arial"):
    return (f'<w:rPr><w:rFonts w:ascii="{fonte}" w:hAnsi="{fonte}" w:cs="{fonte}" w:eastAsia="{fonte}"/>'
            + ("<w:b/><w:bCs/>" if negrito else "") + ("<w:i/><w:iCs/>" if italico else "")
            + ("<w:caps/>" if caps else "") + f'<w:color w:val="{cor}"/><w:sz w:val="{tam}"/><w:szCs w:val="{tam}"/></w:rPr>')


def _estilo(sid, nome, ppr="", rpr="", base="Normal", tipo="paragraph", proximo=None, extra=""):
    return (f'<w:style w:type="{tipo}" w:customStyle="1" w:styleId="{sid}"><w:name w:val="{nome}"/>'
            + (f'<w:basedOn w:val="{base}"/>' if base else "") + (f'<w:next w:val="{proximo}"/>' if proximo else "")
            + f'<w:qFormat/>{extra}<w:pPr>{ppr}</w:pPr>{rpr}</w:style>')


ESTILOS = {
    "BodyText": _estilo("BodyText", "Body Text", LINHA_15 + '<w:ind w:firstLine="709"/><w:jc w:val="both"/>', _rpr()),
    "FirstParagraph": _estilo("FirstParagraph", "First Paragraph", "", "", base="BodyText", proximo="BodyText"),
    "Compact": _estilo("Compact", "Compact", LINHA_1 + '<w:ind w:firstLine="0"/><w:jc w:val="left"/>', _rpr(19)),
    "Heading1": _estilo("Heading1", "heading 1", '<w:keepNext/><w:keepLines/><w:pageBreakBefore/>'
                        '<w:spacing w:before="0" w:after="240" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="0"/>',
                        _rpr(24, negrito=True), proximo="BodyText"),
    "Heading2": _estilo("Heading2", "heading 2", '<w:keepNext/><w:keepLines/>'
                        '<w:spacing w:before="240" w:after="120" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="1"/>',
                        _rpr(24, negrito=True), proximo="BodyText"),
    "Heading3": _estilo("Heading3", "heading 3", '<w:keepNext/><w:keepLines/>'
                        '<w:spacing w:before="200" w:after="80" w:line="360" w:lineRule="auto"/><w:outlineLvl w:val="2"/>',
                        _rpr(24, italico=True, negrito=True), proximo="BodyText"),
    "Capa": _estilo("Capa", "Capa", '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/>',
                    _rpr(24, negrito=True, caps=True)),
    "CapaTitulo": _estilo("CapaTitulo", "Capa titulo", '<w:spacing w:before="0" w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/>',
                          _rpr(28, negrito=True, caps=True)),
    "CapaTexto": _estilo("CapaTexto", "Capa texto", '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/><w:jc w:val="center"/>',
                         _rpr(24)),
    "TituloPre": _estilo("TituloPre", "Titulo pretextual", '<w:keepNext/><w:pageBreakBefore/><w:spacing w:before="0" w:after="360"/><w:jc w:val="center"/>',
                         _rpr(24, negrito=True, caps=True)),
    "Legenda": _estilo("Legenda", "Legenda", '<w:keepNext/><w:keepLines/><w:spacing w:before="200" w:after="60" w:line="240" w:lineRule="auto"/>'
                       '<w:ind w:firstLine="0"/><w:jc w:val="center"/>', _rpr(20, negrito=True)),
    "Fonte": _estilo("Fonte", "Fonte", '<w:spacing w:before="60" w:after="200" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>',
                     _rpr(20)),
    "Figura": _estilo("Figura", "Figura", '<w:keepNext/><w:spacing w:before="0" w:after="0"/><w:ind w:firstLine="0"/><w:jc w:val="center"/>', _rpr()),
    "TituloQuadro": _estilo("TituloQuadro", "Titulo de quadro", '<w:keepNext/><w:spacing w:before="160" w:after="60" w:line="240" w:lineRule="auto"/>'
                            '<w:ind w:firstLine="0"/><w:jc w:val="left"/>', _rpr(21, negrito=True)),
    "Destaque": _estilo("Destaque", "Destaque", '<w:pBdr><w:top w:val="single" w:sz="6" w:space="4" w:color="5B3A29"/>'
                        '<w:left w:val="single" w:sz="6" w:space="4" w:color="5B3A29"/><w:bottom w:val="single" w:sz="6" w:space="4" w:color="5B3A29"/>'
                        '<w:right w:val="single" w:sz="6" w:space="4" w:color="5B3A29"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="F6F3EF"/>'
                        '<w:spacing w:before="60" w:after="60" w:line="300" w:lineRule="auto"/><w:ind w:left="113" w:right="113" w:firstLine="0"/><w:jc w:val="both"/>',
                        _rpr(22)),
    "Sumario1": _estilo("Sumario1", "Sumario 1", '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9061"/></w:tabs>'
                        '<w:spacing w:before="60" w:after="0" w:line="300" w:lineRule="auto"/><w:ind w:left="0" w:hanging="0"/>',
                        _rpr(24, negrito=True)),
    "Sumario2": _estilo("Sumario2", "Sumario 2", '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9061"/></w:tabs>'
                        '<w:spacing w:before="0" w:after="0" w:line="300" w:lineRule="auto"/><w:ind w:left="340"/>', _rpr(24)),
    "Lista": _estilo("Lista", "Lista de ilustracoes", '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9061"/></w:tabs>'
                     '<w:spacing w:before="0" w:after="40" w:line="276" w:lineRule="auto"/><w:ind w:left="1134" w:hanging="1134"/>', _rpr(22)),
    "Assinatura": _estilo("Assinatura", "Assinatura", '<w:spacing w:before="480" w:after="0"/><w:ind w:firstLine="0"/>', _rpr(22)),
    "AssinaturaNome": _estilo("AssinaturaNome", "Assinatura nome", '<w:spacing w:before="0" w:after="0"/><w:ind w:firstLine="0"/>', _rpr(22)),
    "SourceCode": _estilo("SourceCode", "Source Code", '<w:shd w:val="clear" w:color="auto" w:fill="F4F4F4"/><w:wordWrap w:val="off"/>'
                          '<w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/>',
                          _rpr(17, fonte="Consolas")),
}

TABELA = ('<w:style w:type="table" w:default="1" w:styleId="Table"><w:name w:val="Table"/><w:basedOn w:val="TableNormal"/><w:qFormat/>'
          '<w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/><w:jc w:val="left"/></w:pPr>'
          + _rpr(19) +
          '<w:tblPr><w:tblInd w:w="0" w:type="dxa"/><w:tblBorders>'
          '<w:top w:val="single" w:sz="8" w:space="0" w:color="5B3A29"/><w:bottom w:val="single" w:sz="8" w:space="0" w:color="5B3A29"/>'
          '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="BFB3A8"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="BFB3A8"/>'
          '<w:left w:val="single" w:sz="4" w:space="0" w:color="BFB3A8"/><w:right w:val="single" w:sz="4" w:space="0" w:color="BFB3A8"/>'
          '</w:tblBorders><w:tblCellMar><w:top w:w="28" w:type="dxa"/><w:left w:w="85" w:type="dxa"/><w:bottom w:w="28" w:type="dxa"/>'
          '<w:right w:w="85" w:type="dxa"/></w:tblCellMar></w:tblPr>'
          '<w:tblStylePr w:type="firstRow"><w:rPr><w:b/><w:bCs/></w:rPr><w:tblPr/><w:trPr><w:tblHeader/></w:trPr>'
          '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="EDE5DC"/><w:vAlign w:val="bottom"/></w:tcPr></w:tblStylePr></w:style>')

DEFAULTS = ('<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial" w:eastAsia="Arial"/>'
            '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="pt-BR" w:eastAsia="pt-BR" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="120"/></w:pPr></w:pPrDefault></w:docDefaults>')

RODAPE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
          '<w:p><w:pPr><w:jc w:val="right"/></w:pPr>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr><w:t>1</w:t></w:r>'
          '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>'
          '</w:p></w:ftr>')

# A4, margens superior/esquerda 3 cm e inferior/direita 2 cm; rodapé com número; capa sem número (titlePg)
SECAO = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdRodape1"/>'
         '<w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" '
         'w:header="709" w:footer="567" w:gutter="0"/><w:titlePg/></w:sectPr>')


def criar(pandoc, destino):
    destino = Path(destino)
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "base.docx"
        subprocess.run([pandoc, "-o", str(base), "--print-default-data-file", "reference.docx"], check=True)
        pasta = Path(tmp) / "x"
        with zipfile.ZipFile(base) as z:
            z.extractall(pasta)
        estilos = (pasta / "word/styles.xml").read_text(encoding="utf-8")
        estilos = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", DEFAULTS, estilos, flags=re.S)
        for sid in list(ESTILOS) + ["Table", "Title", "Subtitle", "Hyperlink"]:
            estilos = re.sub(r'<w:style [^>]*w:styleId="' + sid + r'".*?</w:style>', "", estilos, flags=re.S)
        estilos = estilos.replace("</w:styles>", "".join(ESTILOS.values()) + TABELA
                                  + '<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
                                    '<w:rPr><w:color w:val="1F4E79"/><w:u w:val="none"/></w:rPr></w:style></w:styles>')
        # títulos padrão do pandoc em preto (Title/Subtitle não são usados: a capa é montada com estilos próprios)
        estilos = re.sub(r'<w:color w:val="[0-9A-F]{6}" w:themeColor="accent1"[^/]*/>', '<w:color w:val="000000"/>', estilos)
        (pasta / "word/styles.xml").write_text(estilos, encoding="utf-8")

        doc = (pasta / "word/document.xml").read_text(encoding="utf-8")
        doc = re.sub(r"<w:body>.*</w:body>", "<w:body><w:p/>" + SECAO + "</w:body>", doc, flags=re.S)
        (pasta / "word/document.xml").write_text(doc, encoding="utf-8")
        (pasta / "word/footer1.xml").write_text(RODAPE, encoding="utf-8")

        rels = (pasta / "word/_rels/document.xml.rels").read_text(encoding="utf-8")
        rels = rels.replace("</Relationships>", '<Relationship Id="rIdRodape1" '
                            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" '
                            'Target="footer1.xml"/></Relationships>')
        (pasta / "word/_rels/document.xml.rels").write_text(rels, encoding="utf-8")
        tipos = (pasta / "[Content_Types].xml").read_text(encoding="utf-8")
        tipos = tipos.replace("</Types>", '<Override PartName="/word/footer1.xml" '
                              'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
        (pasta / "[Content_Types].xml").write_text(tipos, encoding="utf-8")

        destino.parent.mkdir(parents=True, exist_ok=True)
        if destino.exists():
            destino.unlink()
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(pasta.rglob("*")):
                if f.is_file():
                    z.write(f, f.relative_to(pasta).as_posix())
    return destino


if __name__ == "__main__":
    import sys
    print(criar(sys.argv[1] if len(sys.argv) > 1 else shutil.which("pandoc"), "referencia.docx"))
