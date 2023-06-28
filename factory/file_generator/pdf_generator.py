from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.validators import Auto

class PDFGenerator:
    def __init__(self, sim_controller):
        self.sim_controller = sim_controller
        pass

    def get_simulated_routes_number(self):
        pass

    def get_simulated_stops_number(self):
        pass

    def get_simulated_distance(self):
        pass

    def get_bus_commercial_speed(self,bus):
        pass