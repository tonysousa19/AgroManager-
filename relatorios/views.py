import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.units import cm
from maquinas.models import Maquina


def relatorio_maquinas_manutencoes(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    elements = []
    styles = getSampleStyleSheet()

    style_title = styles["Title"]
    style_heading = styles["Heading2"]
    style_normal = styles["Normal"]

    style_wrapped = ParagraphStyle(
        name="Wrapped",
        parent=style_normal,
        fontSize=9,
        leading=11,
        spaceAfter=2,
    )

    # Título do relatório
    elements.append(Paragraph("Relatório de Máquinas e Manutenções", style_title))
    elements.append(Spacer(1, 0.3 * cm))

    maquinas = Maquina.objects.prefetch_related("manutencoes").all()

    for maquina in maquinas:
        elements.append(Paragraph(
            f"<b>Máquina:</b> {maquina.nome} ({maquina.condicao}, {maquina.ano})",
            style_heading,
        ))
        elements.append(Paragraph(
            f"<b>Número de Série:</b> {maquina.numero_de_serie}",
            style_normal,
        ))
        elements.append(Spacer(1, 0.2 * cm))

        manutencoes = maquina.manutencoes.all()
        if manutencoes:
            data = [[
                Paragraph("<b>Data</b>", style_wrapped),
                Paragraph("<b>Descrição</b>", style_wrapped),
                Paragraph("<b>Peças</b>", style_wrapped),
                Paragraph("<b>Custo</b>", style_wrapped),
            ]]

            for m in manutencoes:
                data.append([
                    Paragraph(m.data.strftime("%d/%m/%Y"), style_wrapped),
                    Paragraph(m.descricao or "-", style_wrapped),
                    Paragraph(m.pecas_usadas or "-", style_wrapped),
                    Paragraph(f"R$ {m.custo:.2f}", style_wrapped),
                ])

            table = Table(
                data,
                colWidths=[2.5 * cm, 8.5 * cm, 4 * cm, 2.5 * cm]
            )
            table.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))

            elements.append(table)
        else:
            elements.append(Paragraph("<i>Sem manutenções registradas.</i>", style_normal))

        # Pequeno espaço entre máquinas
        elements.append(Spacer(1, 0.4 * cm))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="relatorio_maquinas_manutencoes.pdf"'
    return response

