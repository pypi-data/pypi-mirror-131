## -*- coding: utf-8; -*-
<%inherit file="/configure.mako" />

<%def name="page_content()">
  ${parent.page_content()}

  <h3 class="block is-size-3">Supported Workflows</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_receiving_from_scratch']"
                  @input="settingsNeedSaved = true">
        From Scratch
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_receiving_from_invoice']"
                  @input="settingsNeedSaved = true">
        From Invoice
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_receiving_from_purchase_order']"
                  @input="settingsNeedSaved = true">
        From Purchase Order
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_receiving_from_purchase_order_with_invoice']"
                  @input="settingsNeedSaved = true">
        From Purchase Order, with Invoice
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_truck_dump_receiving']"
                  @input="settingsNeedSaved = true">
        Truck Dump
      </b-checkbox>
    </b-field>

  </div>

  <h3 class="block is-size-3">Product Handling</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="NB. Allow Cases setting also affects Ordering behavior.">
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_cases']"
                  @input="settingsNeedSaved = true">
        Allow Cases
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.allow_expired_credits']"
                  @input="settingsNeedSaved = true">
        Allow "Expired" Credits
      </b-checkbox>
    </b-field>

  </div>

  <h3 class="block is-size-3">Mobile Interface</h3>
  <div class="block" style="padding-left: 2rem;">

    <b-field message="TODO: this may also affect Ordering (?)">
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.mobile_images']"
                  @input="settingsNeedSaved = true">
        Show Product Images
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.mobile_quick_receive']"
                  @input="settingsNeedSaved = true">
        Allow "Quick Receive"
      </b-checkbox>
    </b-field>

    <b-field>
      <b-checkbox v-model="simpleSettings['rattail.batch.purchase.mobile_quick_receive_all']"
                  @input="settingsNeedSaved = true">
        Allow "Quick Receive All"
      </b-checkbox>
    </b-field>

  </div>
</%def>


${parent.body()}
