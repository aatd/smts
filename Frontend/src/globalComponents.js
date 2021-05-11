import BaseInput    from 'src/components/Inputs/BaseInput.vue'
import BaseCheckbox from 'src/components/Inputs/BaseCheckbox.vue'
import BaseRadio    from 'src/components/Inputs/BaseRadio.vue'
import BaseDropdown from 'src/components/BaseDropdown.vue'
import Card         from 'src/components/Cards/Card.vue'

const GlobalComponents = {
  install (Vue) {
    Vue.component(BaseInput.name,    BaseInput    )
    Vue.component(BaseCheckbox.name, BaseCheckbox )
    Vue.component(BaseRadio.name,    BaseRadio    )
    Vue.component(BaseDropdown.name, BaseDropdown )
    Vue.component(Card.name,         Card         )
  }
}

export default GlobalComponents;