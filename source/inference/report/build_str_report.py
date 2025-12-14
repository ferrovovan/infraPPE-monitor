# build_str_report_extended.py
from typing import Dict, Literal
from .report_type import Report


class ReportBuilder:
	"""Класс для построения отчётов в разных форматах"""
	
	DEFAULT_RISKS = {
		"Hardhat": "~40% (риск ЧМТ)",
		"Safety Vest": "~50% (риск механической травмы)",
		"Gloves": "~35% (риск травм рук)",
		"Goggles": "~60% (риск повреждения глаз)",
		"Mask": "~70% (риск заболеваний дыхательной системы)",
		"Safety Shoes": "~45% (риск травмы стопы)",
		"Ear Protection": "~55% (риск потери слуха)"
	}
	
	def __init__(
		self,
		location: str,
		risk_descriptions: Dict[str, str] | None = None
	):
		self.location = location
		self.risks = risk_descriptions or self.DEFAULT_RISKS
		
	def build(
		self,
		report: Report,
		format_type: Literal["detailed", "short", "html"] = "detailed"
	) -> str:
		"""Построить отчёт в указанном формате"""
		if format_type == "detailed":
			return self._build_detailed(report)
		elif format_type == "short":
			return self._build_short(report)
		elif format_type == "html":
			return self._build_html(report)
		else:
			raise ValueError(f"Неизвестный формат: {format_type}")
	
	def _build_detailed(self, report: Report) -> str:
		"""Детализированный текстовый отчёт"""
		raise NotImplementedError("Метод _build_detailed не определён")
		# return build_str_report(report, self.location, self.risks)
	
	def _build_short(self, report: Report) -> str:
		"""Краткий отчёт (для мгновенного ознакомления)"""
		summary = report['summary']
		lines = []
		
		lines.append(f"📋 Отчёт ТБ | {self.location} | Кадр #{report['frame_id']}\n")
		lines.append(f"👥 Работников: {summary['workers_count']}\n")
		lines.append(f"⚠️  Нарушителей: {summary['violations_count']}\n")
		
		if summary['violations_count'] > 0:
			lines.append("\nНарушения:")
			for worker in report['workers']:
				if worker['missing']:
					lines.append(f"  👷 #{worker['id']}: {', '.join(worker['missing'])}")
		
		return "\n".join(lines)
	
	def _build_html(self, report: Report) -> str:
		"""HTML версия отчёта"""
		summary = report['summary']
		
		html = f"""
		<!DOCTYPE html>
		<html>
		<head>
			<meta charset="UTF-8">
			<title>Отчёт ТБ - {self.location}</title>
			<style>
				body {{ font-family: Arial, sans-serif; margin: 20px; }}
				.header {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
				.violation {{ color: #d32f2f; font-weight: bold; }}
				.ok {{ color: #388e3c; font-weight: bold; }}
				table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
				th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
				th {{ background-color: #f2f2f2; }}
				tr:nth-child(even) {{ background-color: #f9f9f9; }}
			</style>
		</head>
		<body>
			<div class="header">
				<h1>📋 Отчёт по технике безопасности</h1>
				<p><strong>Цех/зона:</strong> {self.location}</p>
				<p><strong>Кадр:</strong> #{report['frame_id']}</p>
			</div>
			
			<h2>📊 Статистика</h2>
			<ul>
				<li>Всего работников: {summary['workers_count']}</li>
				<li>Нарушителей: <span class="violation">{summary['violations_count']}</span></li>
				<li>Без нарушений: <span class="ok">{summary['workers_count'] - summary['violations_count']}</span></li>
			</ul>
			
			<h2>👷 Детализация</h2>
			<table>
				<tr>
					<th>ID работника</th>
					<th>Надеты</th>
					<th>Отсутствуют</th>
					<th>Статус</th>
				</tr>
		"""
		
		for worker in report['workers']:
			status_class = "ok" if not worker['missing'] else "violation"
			status_text = "✅ OK" if not worker['missing'] else "⚠️ Нарушение"
			
			present = ", ".join(worker['present']) if worker['present'] else "—"
			missing = ", ".join(worker['missing']) if worker['missing'] else "—"
			
			html += f"""
				<tr>
					<td>{worker['id']}</td>
					<td>{present}</td>
					<td>{missing}</td>
					<td class="{status_class}">{status_text}</td>
				</tr>
			"""
		
		html += """
			</table>
			
			<h2>📈 Распределение нарушений</h2>
			<ul>
		"""
		
		# Статистика по СИЗ
		missing_stats = {}
		for worker in report['workers']:
			for ppe in worker['missing']:
				missing_stats[ppe] = missing_stats.get(ppe, 0) + 1
		
		for ppe, count in sorted(missing_stats.items(), key=lambda x: x[1], reverse=True):
			percentage = (count / summary['workers_count']) * 100
			risk = self.risks.get(ppe, "риск не указан")
			html += f'<li><strong>{ppe}:</strong> {count} нарушений ({percentage:.1f}%) - {risk}</li>'
		
		html += """
			</ul>
			
			<hr>
			<p><em>Отчёт сгенерирован автоматически</em></p>
		</body>
		</html>
		"""
		
		return html


# Альтернативный вариант для быстрого использования
def build_quick_report(report: Report, location: str) -> str:
	"""Быстрый отчёт без детализации рисков"""
	builder = ReportBuilder(location)
	return builder.build(report, format_type="short")


def build_html_report(report: Report, location: str, risks: Dict[str, str] = None) -> str:
	"""HTML отчёт"""
	builder = ReportBuilder(location, risks)
	return builder.build(report, format_type="html")
