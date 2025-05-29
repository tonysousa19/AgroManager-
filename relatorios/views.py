import io
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.shortcuts import render
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
from django.db.models import Q
from datetime import datetime

def pagina_relatorio(request):
    if not request.user.has_permissao("ver_dashboard"):
        return render(request, 'paginas/permissao/falha_permissao.html')
    
    return render(request, 'paginas/relatorios/gerar_relatorios.html')

def relatorio_maquinas_manutencoes(request):
    if not request.user.has_permissao("ver_dashboard"):
        return render(request, 'paginas/permissao/falha_permissao.html')
    
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

    nome = request.GET.get('nome', '')
    condicao = request.GET.get('condicao', '')
    ano = request.GET.get('ano', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    filtros = Q()
    
    if nome:
        filtros &= Q(nome__icontains=nome)
    if condicao:
        filtros &= Q(condicao=condicao)
    if ano:
        filtros &= Q(ano=ano)
    
    maquinas = Maquina.objects.prefetch_related("manutencoes").filter(filtros)
    
    titulo = "Relatório de Máquinas e Manutenções"
    filtros_info = []
    
    if nome:
        filtros_info.append(f"Nome: {nome}")
    if condicao:
        filtros_info.append(f"Condição: {condicao}")
    if ano:
        filtros_info.append(f"Ano: {ano}")
    if data_inicio:
        filtros_info.append(f"De: {data_inicio}")
    if data_fim:
        filtros_info.append(f"Até: {data_fim}")
    
    if filtros_info:
        titulo += " - Filtros: " + ", ".join(filtros_info)
    
    elements.append(Paragraph(titulo, style_title))
    elements.append(Spacer(1, 0.3 * cm))

    for maquina in maquinas:
        manutencoes = maquina.manutencoes.all()
        
        if data_inicio or data_fim:
            man_filtros = Q()
            if data_inicio:
                try:
                    data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                    man_filtros &= Q(data__gte=data_inicio_obj)
                except ValueError:
                    pass
            if data_fim:
                try:
                    data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                    man_filtros &= Q(data__lte=data_fim_obj)
                except ValueError:
                    pass
            
            manutencoes = manutencoes.filter(man_filtros)
        
        elements.append(Paragraph(
            f"<b>Máquina:</b> {maquina.nome} ({maquina.condicao}, {maquina.ano})",
            style_heading,
        ))
        elements.append(Paragraph(
            f"<b>Número de Série:</b> {maquina.numero_de_serie}",
            style_normal,
        ))
        elements.append(Spacer(1, 0.2 * cm))

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

        elements.append(Spacer(1, 0.4 * cm))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="relatorio_maquinas_manutencoes.pdf"'
    return response


