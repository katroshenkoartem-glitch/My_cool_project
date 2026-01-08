<template>
  <div
    class="bg-white border-2 border-gray-100 rounded-none p-6 shadow-sm hover:border-gray-300 transition-colors"
  >
    <div class="flex gap-6">
      <div class="w-24 h-24 flex-shrink-0">
        <img
          :src="item.image_url"
          :alt="item.name"
          class="w-full h-full object-cover rounded-none"
          @error="handleImageError"
        />
      </div>

      <div class="flex-grow">
        <h3 class="text-lg font-bold text-black mb-2">
          {{ item.name || 'Название товара' }}
        </h3>
        <p class="text-gray-600 text-sm mb-3">${{ formattedPrice }} each</p>

        <div class="flex items-center gap-4">
          <div class="flex items-center border-2 border-gray-100 rounded-none" style="color: black">
            <button
              @click="decreaseQuantity"
              :disabled="updating"
              class="px-3 py-2 hover:bg-gray-100 transition-colors disabled:opacity-50"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>

            <span class="px-4 py-2 font-medium min-w-[40px] text-center">
              {{ item.quantity }}
            </span>

            <button
              @click="increaseQuantity"
              :disabled="updating"
            class="px-3 py-2 hover:bg-gray-100 transition-colors disabled:opacity-50"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
          </div>

          <button
            @click="handleRemove"
            :disabled="updating"
            class="text-red-600 hover:text-red-700 transition-colors disabled:opacity-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <div class="text-right">
        <p class="text-xl font-bold text-black">${{ formattedSubtotal }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '@/stores/cart'

// Props
const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
})

// State
const cartStore = useCartStore()
const updating = ref(false)

/**
 * Безопасное форматирование цены за штуку
 */
const formattedPrice = computed(() => {
  const price = Number(props.item.price) || 0
  return price.toFixed(2)
})

/**
 * Безопасное форматирование общей суммы (Subtotal)
 * Если бэкенд не прислал subtotal, рассчитываем его сами
 */
const formattedSubtotal = computed(() => {
  if (props.item.subtotal !== undefined && props.item.subtotal !== null) {
    return Number(props.item.subtotal).toFixed(2)
  }
  // Запасной вариант расчета
  const calc = (Number(props.item.price) || 0) * (props.item.quantity || 0)
  return calc.toFixed(2)
})

// Methods
async function increaseQuantity() {
  if (updating.value) return
  updating.value = true
  try {
    await cartStore.updateQuantity(props.item.product_id, props.item.quantity + 1)
  } catch (error) {
    console.error('Ошибка при увеличении количества:', error)
  } finally {
    updating.value = false
  }
}

async function decreaseQuantity() {
  if (updating.value) return
  updating.value = true
  try {
    if (props.item.quantity > 1) {
      await cartStore.updateQuantity(props.item.product_id, props.item.quantity - 1)
    } else {
      await cartStore.removeFromCart(props.item.product_id)
    }
  } catch (error) {
    console.error('Ошибка при уменьшении количества:', error)
  } finally {
    updating.value = false
  }
}

async function handleRemove() {
  if (updating.value) return
  updating.value = true
  try {
    await cartStore.removeFromCart(props.item.product_id)
  } catch (error) {
    console.error('Ошибка при удалении товара:', error)
  } finally {
    updating.value = false
  }
}

function handleImageError(event) {
  event.target.src = 'https://via.placeholder.com/100x100?text=No+Image'
}
</script>