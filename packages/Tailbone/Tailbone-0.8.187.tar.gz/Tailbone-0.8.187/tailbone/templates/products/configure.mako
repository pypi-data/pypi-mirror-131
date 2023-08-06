## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <h3 class="block is-size-3">Key Field</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field grouped>

      <b-field label="Key Field">
        <b-select name="rattail.product.key"
                  v-model="simpleSettings['rattail.product.key']"
                  @input="updateKeyTitle()">
          <option value="upc">upc</option>
          <option value="item_id">item_id</option>
          <option value="scancode">scancode</option>
        </b-select>
      </b-field>

      <b-field label="Key Field Label">
        <b-input name="rattail.product.key_title"
                 v-model="simpleSettings['rattail.product.key_title']"
                 @input="settingsNeedSaved = true">
        </b-input>
      </b-field>

    </b-field>

  </div>

  <h3 class="block is-size-3">Display</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="If a product has an image in the DB, that will still be preferred.">
      <b-checkbox name="tailbone.products.show_pod_image"
                  v-model="simpleSettings['tailbone.products.show_pod_image']"
                  @input="settingsNeedSaved = true">
        Show "POD" Images as fallback
      </b-checkbox>
    </b-field>

  </div>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPage.methods.getTitleForKey = function(key) {
        switch (key) {
        case 'item_id':
            return "Item ID"
        case 'scancode':
            return "Scancode"
        default:
            return "UPC"
        }
    }

    ThisPage.methods.updateKeyTitle = function() {
        this.simpleSettings['rattail.product.key_title'] = this.getTitleForKey(
            this.simpleSettings['rattail.product.key'])
        this.settingsNeedSaved = true
    }

  </script>
</%def>


${parent.body()}
