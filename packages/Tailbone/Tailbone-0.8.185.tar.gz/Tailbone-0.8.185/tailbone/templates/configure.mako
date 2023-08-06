## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">Configure ${config_title}</%def>

<%def name="save_undo_buttons()">
  <div class="buttons"
       v-if="settingsNeedSaved">
    <b-button type="is-primary"
              @click="saveSettings"
              :disabled="savingSettings"
              icon-pack="fas"
              icon-left="save">
      {{ savingSettings ? "Working, please wait..." : "Save All Settings" }}
    </b-button>
    <once-button tag="a" href="${request.current_route_url()}"
                 @click="undoChanges = true"
                 icon-left="undo"
                 text="Undo All Changes">
    </once-button>
  </div>
</%def>

<%def name="purge_button()">
  <b-button type="is-danger"
            @click="purgeSettingsInit()"
            icon-pack="fas"
            icon-left="trash">
    Remove All Settings
  </b-button>
</%def>

<%def name="buttons_row()">
  <div class="level">
    <div class="level-left">

      <div class="level-item">
        <p class="block">
          This tool lets you modify the ${config_title} configuration.
        </p>
      </div>

      <div class="level-item">
        ${self.save_undo_buttons()}
      </div>
    </div>

    <div class="level-right">
      <div class="level-item">
        ${self.purge_button()}
      </div>
    </div>
  </div>
</%def>

<%def name="page_content()">
  ${parent.page_content()}

  <br />

  ${self.buttons_row()}

  <b-modal has-modal-card
           :active.sync="purgeSettingsShowDialog">
    <div class="modal-card">

      <header class="modal-card-head">
        <p class="modal-card-title">Remove All Settings</p>
      </header>

      <section class="modal-card-body">
        <p class="block">
          If you like we can remove all settings for ${config_title}
          from the DB.
        </p>
        <p class="block">
          Note that the tool normally removes all settings first,
          every time you click "Save Settings" - here though you can
          "just remove and not save" the settings.
        </p>
        <p class="block">
          Note also that this will of course 
          <span class="is-italic">not</span> remove any settings from
          your config files, so after removing from DB,
          <span class="is-italic">only</span> your config file
          settings should be in effect.
        </p>
      </section>

      <footer class="modal-card-foot">
        <b-button @click="purgeSettingsShowDialog = false">
          Cancel
        </b-button>
        ${h.form(request.current_route_url())}
        ${h.csrf_token(request)}
        ${h.hidden('remove_settings', 'true')}
        <b-button type="is-danger"
                  native-type="submit"
                  :disabled="purgingSettings"
                  icon-pack="fas"
                  icon-left="trash"
                  @click="purgingSettings = true">
          {{ purgingSettings ? "Working, please wait..." : "Remove All Settings" }}
        </b-button>
        ${h.end_form()}
      </footer>
    </div>
  </b-modal>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    % if simple_settings is not Undefined:
        ThisPageData.simpleSettings = ${json.dumps(simple_settings)|n}
    % endif

    ThisPageData.purgeSettingsShowDialog = false
    ThisPageData.purgingSettings = false

    ThisPageData.settingsNeedSaved = false
    ThisPageData.undoChanges = false
    ThisPageData.savingSettings = false

    ThisPage.methods.purgeSettingsInit = function() {
        this.purgeSettingsShowDialog = true
    }

    ThisPage.methods.settingsCollectParams = function() {
        % if simple_settings is not Undefined:
            return {simple_settings: this.simpleSettings}
        % else:
            return {}
        % endif
    }

    ThisPage.methods.saveSettings = function() {
        this.savingSettings = true

        let url = ${json.dumps(request.current_route_url())|n}
        let params = this.settingsCollectParams()
        let headers = {
            'X-CSRF-TOKEN': this.csrftoken,
        }

        this.$http.post(url, params, {headers: headers}).then((response) => {
            if (response.data.success) {
                this.settingsNeedSaved = false
                location.href = url // reload page
            } else {
                this.$buefy.toast.open({
                    message: "Save failed:  " + (response.data.error || "(unknown error)"),
                    type: 'is-danger',
                    duration: 4000, // 4 seconds
                })
            }
        }).catch((error) => {
            this.$buefy.toast.open({
                message: "Save failed:  (unknown error)",
                type: 'is-danger',
                duration: 4000, // 4 seconds
            })
        })
    }

    // cf. https://stackoverflow.com/a/56551646
    ThisPage.methods.beforeWindowUnload = function(e) {
        if (this.settingsNeedSaved && !this.undoChanges) {
            e.preventDefault()
            e.returnValue = ''
        }
    }

    ThisPage.created = function() {
        window.addEventListener('beforeunload', this.beforeWindowUnload)
    }

  </script>
</%def>


${parent.body()}
