import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface BusinessSettings {
    startTime: string; // HH:mm
    endTime: string;   // HH:mm
    intervalMinutes: number;
    closedDays: number[]; // 0: Sun, 1: Mon, ...
    breakStartTime: string;
    breakEndTime: string;
    hasBreak: boolean;
}

export interface SavedAppointment {
    id: string
    cancel_token: string | null
    service_name: string
    company_name: string
    sector_name: string
    staff_name: string
    date: string
    time: string
    amount: number
    status: 'Beklemede' | 'Kesinleşti' | 'İptal Edildi' | 'Ödeme Başarısız' | 'Tamamlandı'
    created_at: string
    theme_accent: string
}

export const useAppointmentStore = defineStore('appointment', () => {

    const sectors = ref<any[]>([])
    const companies = ref<any[]>([])
    const staffList = ref<any[]>([])
    const businessSettings = ref<BusinessSettings>({
        startTime: '09:00',
        endTime: '19:00',
        intervalMinutes: 60,
        closedDays: [0],
        breakStartTime: '12:00',
        breakEndTime: '13:00',
        hasBreak: true
    })
    const isDataLoaded = ref(false)
    const reviews = ref<any[]>([])
    
    // Auth State (Instant Reactivity)
    const currentUser = ref<any>(JSON.parse(localStorage.getItem('dita_customer_user') || sessionStorage.getItem('dita_customer_user') || 'null'))
    const setCurrentUser = (user: any) => {
        currentUser.value = user
    }

    const fetchInitialData = async () => {
        try {
            const [sectorsRes, staffRes, reviewsRes, companiesRes] = await Promise.all([
                fetch('/api/sectors'),
                fetch('/api/staff'),
                fetch('/api/reviews'),
                fetch('/api/companies')
            ])
            sectors.value = await sectorsRes.json()
            staffList.value = await staffRes.json()
            reviews.value = await reviewsRes.json()
            companies.value = await companiesRes.json()
            isDataLoaded.value = true
        } catch (e) {
            console.error("Failed to fetch initial config", e)
        }
    }

    const selectedSectorId = ref<string | null>(null)
    const selectedCompanyId = ref<string | null>(null)
    const selectedSector = computed(() => sectors.value.find(s => s.id === selectedSectorId.value) || null)
    const currentTheme = computed(() => selectedSector.value?.theme || {
        accent: '#C5A059', accentRgb: '197, 160, 89',
        accentDark: '#9A7A40', accentLight: '#E8D5A3',
        bg: 'rgba(197, 160, 89, 0.05)', cardBg: 'rgba(197, 160, 89, 0.04)', name: 'Gold'
    })

    const selectedStaffName = ref<string | null>(null)
    const selectedDate = ref<Date | null>(null)
    const selectedTime = ref<string | null>(null)

    const saveSettings = async (newSettings: BusinessSettings) => {
        // Obsolete globally. Left here just in case, but settings are now saved via Settings.vue
        businessSettings.value = { ...newSettings }
        if (selectedTime.value && !availableSlots.value.includes(selectedTime.value)) {
            selectedTime.value = null
        }
    }

    const availableSlots = computed(() => {
        const slots: string[] = []
        
        const company = companies.value.find((c: any) => c.id === selectedCompanyId.value)
        const cSettings = company?.settings || businessSettings.value

        // Default settings
        let startStr = cSettings.startTime
        let endStr = cSettings.endTime
        let breakStartStr = cSettings.breakStartTime
        let breakEndStr = cSettings.breakEndTime
        let hasBreak = cSettings.hasBreak

        // If staff is selected, override with staff-specific hours if available
        if (selectedStaffName.value) {
            const staff = staffList.value.find(s => s.name === selectedStaffName.value)
            if (staff && staff.working_hours) {
                startStr = staff.working_hours.startTime || startStr
                endStr = staff.working_hours.endTime || endStr
            }
            if (staff && staff.breaks) {
                breakStartStr = staff.breaks.startTime || breakStartStr
                breakEndStr = staff.breaks.endTime || breakEndStr
                hasBreak = !!staff.breaks.startTime
            }
        }

        if (!startStr) return slots
        const [startH, startM] = startStr.split(':').map(Number)
        const [endH, endM] = endStr.split(':').map(Number)

        let breakStart = -1
        let breakEnd = -1
        if (hasBreak && breakStartStr && breakEndStr) {
            const [bSH, bSM] = breakStartStr.split(':').map(Number)
            const [bEH, bEM] = breakEndStr.split(':').map(Number)
            breakStart = bSH * 60 + bSM
            breakEnd = bEH * 60 + bEM
        }

        let currentTotalMins = startH * 60 + startM
        const endTotalMins = endH * 60 + endM
        const interval = cSettings.intervalMinutes

        while (currentTotalMins + interval <= endTotalMins) {
            const h = Math.floor(currentTotalMins / 60).toString().padStart(2, '0')
            const m = (currentTotalMins % 60).toString().padStart(2, '0')

            if (breakStart !== -1 && currentTotalMins >= breakStart && currentTotalMins < breakEnd) {
                // skip block due to break
            } else {
                slots.push(`${h}:${m}`)
            }
            currentTotalMins += interval
        }
        return slots
    })

    const services = computed(() => {
        const comp = companies.value.find((c: any) => c.id === selectedCompanyId.value)
        if (comp && comp.services && comp.services.length > 0) {
             return comp.services
        }
        return selectedSector.value?.services || []
    })
    const categorizedServices = computed(() => {
        const groups: Record<string, any[]> = {}
        services.value.forEach((s: any) => {
            const cat = s.category || 'Genel'
            if (!groups[cat]) groups[cat] = []
            groups[cat].push(s)
        })
        return groups
    })
    const selectedServiceId = ref<number | null>(null)
    const selectedService = computed(() => services.value.find((s: any) => s.id === selectedServiceId.value) || null)

    const serviceName = computed(() => selectedService.value?.name || '')
    const servicePrice = computed(() => {
        const service = selectedService.value
        if (!service) return 0
        const comp = companies.value.find((c: any) => c.id === selectedCompanyId.value)
        if (comp && comp.custom_prices && comp.custom_prices[service.id]) {
            return comp.custom_prices[service.id]
        }
        return service.price
    })

    const currentBookingStep = ref(0)

    const depositRate = ref(1.0)
    const customerName = ref<string | null>(null)
    const customerPhone = ref<string | null>(localStorage.getItem("dita_user_phone") || null)
    const depositAmount = computed(() => servicePrice.value * depositRate.value)

    const setSelectedDate = (date: Date) => {
        selectedDate.value = date
        selectedTime.value = null
    }
    const setSelectedTime = (time: string) => { selectedTime.value = time }
    const setCustomerInfo = (name: string, phone: string) => {
        customerName.value = name
        customerPhone.value = phone
        localStorage.setItem("dita_user_phone", phone)
    }

    const prepareCheckoutPayload = () => {
        return {
            service_name: serviceName.value || 'Hizmet',
            service_price: servicePrice.value,
            deposit_amount: servicePrice.value,
            staff_name: selectedStaffName.value,
            company_id: selectedCompanyId.value,
            appointment_date: selectedDate.value ? `${selectedDate.value.getFullYear()}-${(selectedDate.value.getMonth() + 1).toString().padStart(2, '0')}-${selectedDate.value.getDate().toString().padStart(2, '0')}` : null,
            appointment_time: selectedTime.value,
            customer_name: customerName.value,
            customer_phone: customerPhone.value
        }
    }

    const appointmentSummary = computed(() => {
        if (!selectedDate.value || !selectedTime.value) return null
        return {
            date: selectedDate.value.toLocaleDateString('tr-TR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }),
            time: selectedTime.value
        }
    })

    const myAppointments = ref<SavedAppointment[]>([])

    const loadMyAppointments = async (phone: string) => {
        try {
            const res = await fetch(`/api/my-appointments?phone=${phone}`)
            if (res.ok) {
                myAppointments.value = await res.json()
            }
        } catch (e) {
            console.error(e)
        }
    }

    const addAppointment = (id: string, cancel_token: string | null) => {
        if (customerPhone.value) {
            setTimeout(() => loadMyAppointments(customerPhone.value!), 1000)
        }
    }

    const cancelAppointmentLocally = (id: string) => {
        const appt = myAppointments.value.find(a => a.id === id)
        if (appt) {
            appt.status = 'İptal Edildi'
            appt.cancel_token = null
        }
    }

    const resetBooking = () => {
        selectedSectorId.value = null
        selectedCompanyId.value = null
        selectedServiceId.value = null
        selectedStaffName.value = null
        selectedDate.value = null
        selectedTime.value = null
        currentBookingStep.value = 0
    }

    const toasts = ref<{ id: string, message: string, type: 'success' | 'error' | 'info' }[]>([])
    
    const addToast = (message: string, type: 'success' | 'error' | 'info' = 'info') => {
        const id = Math.random().toString(36).substr(2, 9)
        toasts.value.push({ id, message, type })
        setTimeout(() => removeToast(id), 3000)
    }

    const removeToast = (id: string) => {
        toasts.value = toasts.value.filter(t => t.id !== id)
    }

    const authOverlay = ref({ visible: false, message: '', type: 'loading' as 'loading' | 'success' })
    const triggerAuthOverlay = (message: string, type: 'loading' | 'success', duration = 1500) => {
        authOverlay.value = { visible: true, message, type }
        if (type === 'success') {
            setTimeout(() => {
                authOverlay.value.visible = false
            }, duration)
        }
    }

    const setOccupiedSlots = (slots: string[]) => {
        // This is a compatibility fix for older builds
        console.log("Setting occupied slots:", slots)
    }

    const setBookedSlots = (slots: string[]) => {
        // Some components might expect this
        console.log("Setting booked slots:", slots)
    }

    return {
        staffList, selectedStaffName, reviews,
        sectors, selectedSectorId, selectedSector, currentTheme,
        companies, selectedCompanyId,
        selectedDate, selectedTime, availableSlots,
        services, selectedServiceId, selectedService, categorizedServices,
        serviceName, servicePrice,
        depositRate, customerName, customerPhone, depositAmount,
        setSelectedDate, setSelectedTime, setCustomerInfo,
        prepareCheckoutPayload, appointmentSummary,
        currentBookingStep,
        myAppointments, addAppointment, cancelAppointmentLocally, loadMyAppointments,
        businessSettings, saveSettings, fetchInitialData, isDataLoaded,
        resetBooking,
        toasts, addToast, removeToast,
        authOverlay, triggerAuthOverlay,
        currentUser, setCurrentUser,
        setOccupiedSlots, setBookedSlots
    }
})
