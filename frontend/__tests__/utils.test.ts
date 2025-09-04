/**
 * Basic utility tests for Nada Records Techno Store
 */

describe('Basic Utilities', () => {
  it('should perform basic JavaScript operations', () => {
    expect(1 + 1).toBe(2)
    expect('hello'.toUpperCase()).toBe('HELLO')
    expect([1, 2, 3].length).toBe(3)
  })

  it('should handle string operations', () => {
    const testString = 'Nada Records Techno Store'
    expect(testString.toLowerCase()).toContain('nada')
    expect(testString.split(' ')).toHaveLength(4)
  })

  it('should handle array operations', () => {
    const testArray = ['techno', 'house', 'ambient']
    expect(testArray).toContain('techno')
    expect(testArray.filter(genre => genre.length > 5)).toHaveLength(2)
  })

  it('should handle object operations', () => {
    const testObject = {
      store: 'Nada Records',
      genre: 'Techno',
      established: 2024
    }

    expect(testObject.store).toBe('Nada Records')
    expect(Object.keys(testObject)).toHaveLength(3)
    expect(testObject.established).toBeGreaterThan(2020)
  })

  it('should handle async operations', async () => {
    const asyncFunction = async () => {
      return Promise.resolve('test complete')
    }

    const result = await asyncFunction()
    expect(result).toBe('test complete')
  })
})

describe('Environment and Setup', () => {
  it('should have access to global objects', () => {
    expect(typeof window).toBe('object')
    expect(typeof document).toBe('object')
    expect(typeof console).toBe('object')
  })

  it('should handle JSON operations', () => {
    const testData = { name: 'test', value: 123 }
    const jsonString = JSON.stringify(testData)
    const parsedData = JSON.parse(jsonString)

    expect(parsedData).toEqual(testData)
    expect(parsedData.name).toBe('test')
  })

  it('should handle error scenarios gracefully', () => {
    expect(() => {
      throw new Error('Test error')
    }).toThrow('Test error')

    try {
      JSON.parse('invalid json')
    } catch (error) {
      expect(error).toBeInstanceOf(SyntaxError)
    }
  })
})
