## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="page_content()">
  ${parent.page_content()}

  <h3 class="block is-size-3">Sending</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.mail.record_attempts']"
                  @input="settingsNeedSaved = true">
        Make record of all attempts to send email
      </b-checkbox>
    </b-field>

  </div>
</%def>


${parent.body()}
