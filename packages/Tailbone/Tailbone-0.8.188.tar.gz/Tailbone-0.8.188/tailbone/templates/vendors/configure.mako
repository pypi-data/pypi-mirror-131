## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="form_content()">

  <h3 class="block is-size-3">Display</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="If not set, vendor chooser is a dropdown field.">
      <b-checkbox name="rattail.vendor.use_autocomplete"
                  v-model="simpleSettings['rattail.vendor.use_autocomplete']"
                  @input="settingsNeedSaved = true">
        Show vendor chooser as autocomplete field
      </b-checkbox>
    </b-field>

  </div>
</%def>


${parent.body()}
