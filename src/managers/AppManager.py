from managers.models.reviewsManager import ReviewsManager
from managers.models.fase1Manager import Fase1Manager
from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric


class AppManagers:
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp):
        self.ReviewsManager = ReviewsManager(Localmetric, ClickUp)
        self.Fase1Manager = Fase1Manager(Localmetric, ClickUp)



