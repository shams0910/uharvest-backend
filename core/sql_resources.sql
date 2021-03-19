-- view name : TaskProgressesOfCropChoiceByTownInDistrictInDate
select tp.task_id, sum(tp.size) as completed_size, contour.town_id, towns.total_size, towns.name, towns.number_of_contours
from core_taskprogress as tp
right join core_crop as crop on tp.crop_id=crop.id
left join core_cropchoice as cropchoice on cropchoice.id=crop.crop_choice_id
left join locations_contour as contour on crop.contour_id=contour.id
right join (
	SELECT town.id, town.name, sum(crop.size) as total_size, count(contour.id) as number_of_contours
	FROM core_crop as crop 
	left JOIN locations_contour as contour ON crop.contour_id = contour.id
	right join locations_town as town on contour.town_id = town.id
	WHERE (crop.crop_choice_id = 1 or crop.crop_choice_id is null) and (crop.year=2021 or crop.year is null) and town.district_id=1 
	group by town.id 
) as towns on contour.town_id = towns.id
where (crop.crop_choice_id=1 or crop.crop_choice_id is null) and (crop.year=2021 or crop.year is null) and (tp.date<='2021-01-16' or tp.date is null)
group by contour.town_id, tp.task_id, towns.id, towns.total_size, towns.name, towns.number_of_contours

-- view name : 