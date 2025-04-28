from pydantic import BaseModel, computed_field
from typing import Dict

class Institute(BaseModel):
    __kai_institutes: Dict[int, str] = {
        1: "Институт авиации, наземного транспорта и энергетики",  # отделение СПО ТК 8
        2: "Факультет физико-математический",
        3: "Институт автоматики и электронного приборостроения",
        4: "Институт компьютерных технологий и защиты информации",  # отделение СПО КИТ 4
        5: "Институт радиоэлектроники, фотоники и цифровых технологий",
        6: "Институт инженерной экономики и предпринимательства"
    }

    institute_num: int

    @computed_field(return_type=str)  # type: ignore[prop-decorator]
    @property
    def institute(self) -> str:
        if self.institute_num == 8:
            return self.__kai_institutes[1]
        elif self.institute_num in self.__kai_institutes:
            return self.__kai_institutes[self.institute_num]
        else:
            raise ValueError(f"Номер института {self.institute_num} не найден в списке.")
