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
                    <option value="LIGHTNING">Lightning</option>
                    <option value="THUNDER">Thunder</option>
                    <option value="POISON">Poison</option>
                    <option value="ICE">Ice</option>
                    <option value="FIRE">Fire</option>
                    <option value="DIVINE">Divine</option>
                    <option value="MAGIC">Magic</option>
                    <option value="SHADOWS">Shadows</option>
                    <option value="RAINBOW">Rainbow</option>
                    <option value="PLASMA">Plasma</option>
                    <option value="ARCANE">Arcane</option>
                    <option value="STORM">Storm</option>
                </select>
            `);
        } else if (category === "Potions") {
            dynamicSelects.append(`
               <select id="type" name="type" required>
                    <option value="" class="option-disabled" disabled selected hidden>Select your potion</option>
                    <option value="HEAL">Heal</option>
                    <option value="POISON">Poison</option>
                    <option value="INVISIBILITY">Invisibility</option>
                    <option value="STRENGTH">Strength</option>
                    <option value="RESISTANCE">Resistance</option>
                    <option value="LUCKY">Lucky</option>
                    <option value="WEAKNESS">Weakness</option>
                    <option value="SLOWNESS">Slowness</option>
                    <option value="FIRE">Fire</option>
                    <option value="REGENERATION">Regenaration</option>
                    <option value="DARKNESS">Darkness</option>
                </select>
            `);
        } else if (category === "Armors") {
            dynamicSelects.append(`
                <select id="type" name="type" required>
                    <option value="" class="option-disabled" disabled selected hidden>Armor type</option>
                    <option value="HELMET">Helmet</option>
                    <option value="CHESTPLATE">Chestplate</option>
                    <option value="ARMS">Arms</option>
                    <option value="LEGGINGS">Leggings</option>
                    <option value="BOOTS">Boots</option>
                </select>
                <select id="armor-material" name="armor-material" required>
                    <option value="" class="option-disabled" disabled selected hidden>Armor material</option>
                    <option value="CLOTH">Cloth</option>
                    <option value="LEATHER">Leather</option>
                    <option value="CHAINMAIL">Chainmail</option>
                    <option value="IRON">Iron</option>
                    <option value="CRYSTAL">Crystal</option>
                </select>
            `);
        }
    });
});