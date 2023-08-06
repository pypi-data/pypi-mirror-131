A package that helps to find various properties of two types of real-estate properties
(Apartments and Family Homes) and display all the relevant information.

**Package: RealEstate**

**Sub-package 1: Apartment: Displays various dettails for apartments.**
+ **Features**
    + class 1 (parent): features
       + apartment_price
       + apartment_area
       + apartment_display
    + class 2 (child): apartment_type
       + floors
       + (all other methods of parent class features)
+ **Location**
    + class: location(child)
        + city
        + locality
        + facing_direction
        + (all methods imported from the parent class, which is in the features module)
+ **Condition**
    + class: apartment_condition(child)
        + maintenance_required
        + discount
        + furnishing_status
        + (all methods imported from the parent class, which is in the features module)
        
**Sub-package 2: FamilyHome: predicts various properties for family homes..**
+ **Attributes**
    + class 1 (parent): characteristics
       + house_price
       + house_area
       + house_display
    + class 2 (child): quality
       + build_quality
       + (all other methods of parent class features)
+ **AreaType**
    + class: areaType (Child)
        + nearby_amenities
        + view
        + population
        + (all methods imported from the parent class, which is in the features module)
+ **highlights**
    + class: highlights(child)
        + garage_capacity
        + swimming_pool_type
        + furnish_type
        + (all methods imported from the parent class, which is in the features module)