$(document).ready(function () {
    $("#category").change(function () {
        var category = $(this).val();
        var dynamicSelects = $("#dynamic-selects");

        dynamicSelects.empty();

        if (category === "Weapons") {
            dynamicSelects.append(`
                <select id="type" name="type" required>
                    <option value="" class="option-disabled" disabled selected hidden>Select your weapon</option>
                    <option value="SWORD">Sword</option>
                    <option value="CROSSBOW">Crossbow</option>
                    <option value="MAGIC WAND">Wand</option>
                    <option value="AXE">Axe</option>
                    <option value="SPEAR">Spear</option>
                    <option value="DAGGER">Dagger</option>
                </select>
                <select id="weapon-element" name="weapon-element" required>
                    <option value="" class="option-disabled" disabled selected hidden>Select an element</option>
                    <option value="lightning">Lightning</option>
                    <option value="thunder">Thunder</option>
                    <option value="poison">Poison</option>
                    <option value="ice">Ice</option>
                    <option value="fire">Fire</option>
                    <option value="divine">Divine</option>
                    <option value="magic">Magic</option>
                    <option value="shadows">Shadows</option>
                    <option value="rainbow">Rainbow</option>
                    <option value="plasma">Plasma</option>
                    <option value="arcane">Arcane</option>
                    <option value="storm">Storm</option>
                </select>
            `);
        } else if (category === "Potions") {
            dynamicSelects.append(`
               <select id="type" name="type" required>
                    <option value="" class="option-disabled" disabled selected hidden>Select your potion</option>
                    <option value="HEAL">Heal</option>
                    <option value="POISON">Poison</option>
                    <option value="INVISIBILITY">Invisibility</option>
                    <option value="SPEED">Speed</option>
                </select>
            `);
        } else if (category === "Armors") {
            dynamicSelects.append(`
                <select id="first-characteristic" name="first-characteristic" required>
                    <option value="" class="option-disabled" disabled selected hidden>Select your armor type</option>
                    <option value="HEAVY">Heavy Armor</option>
                    <option value="LIGHT">Light Armor</option>
                    <option value="MAGIC">Magic Armor</option>
                </select>
            `);
        }
    });
});