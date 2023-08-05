/*! DSFR v1.2.1 | SPDX-License-Identifier: MIT | License-Filename: LICENSE.md | restricted use (see terms and conditions) */

(function () {
  'use strict';

  var config = {
    prefix: 'fr',
    namespace: 'dsfr',
    organisation: '@gouvfr',
    version: '1.2.1'
  };

  var api = window[config.namespace];

  var AccordionSelector = {
    GROUP: api.ns.selector('accordions-group'),
    COLLAPSE: ((api.ns.selector('accordion')) + " > " + (api.ns.selector('collapse')))
  };

  var AccordionsGroup = /*@__PURE__*/(function (superclass) {
    function AccordionsGroup () {
      superclass.apply(this, arguments);
    }

    if ( superclass ) AccordionsGroup.__proto__ = superclass;
    AccordionsGroup.prototype = Object.create( superclass && superclass.prototype );
    AccordionsGroup.prototype.constructor = AccordionsGroup;

    var staticAccessors = { instanceClassName: { configurable: true } };

    staticAccessors.instanceClassName.get = function () {
      return 'AccordionsGroup';
    };

    AccordionsGroup.prototype.validate = function validate (member) {
      return member.node.matches(AccordionSelector.COLLAPSE);
    };

    Object.defineProperties( AccordionsGroup, staticAccessors );

    return AccordionsGroup;
  }(api.core.CollapsesGroup));

  api.accordion = {
    AccordionSelector: AccordionSelector,
    AccordionsGroup: AccordionsGroup
  };

  api.register(api.accordion.AccordionSelector.GROUP, api.accordion.AccordionsGroup);

})();
//# sourceMappingURL=accordion.nomodule.js.map
